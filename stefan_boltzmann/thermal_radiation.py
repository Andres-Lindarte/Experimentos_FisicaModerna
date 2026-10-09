import os 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from scipy import stats

def read_values(file_name: str):
    """
    sep: Means the separation between values, in this case, the space 
    header: Since we don´t have headers on the raw text file
    names: Manually written headers 
    """
    points = pd.read_csv(f"data/{file_name}", sep='\\s+', header=None, names=['V', 'I', 'mV'])
    return points 

def linear_regression(x: list, y: list):
    X=np.array(x) # Convert the list to a numpy array
    Y=np.array(y) 
    X = X.reshape(-1, 1) # Reshape the data to fit the model

    model = LinearRegression() # Create a linear regression model
    model.fit(X, Y) # Fit the model to the data

    slope = model.coef_[0] # Get the slope of the line
    intercept = model.intercept_ # Get the intercept of the line
    r_pearson, _ = stats.pearsonr(x, y) # Calculate the Pearson correlation coefficient
    r_squared = r_pearson**2 # Calculate the R-squared value
    return slope, intercept, r_squared

def grouped_plot(distances, x_data, y_data, slopes, intercepts, markers, colors, folder_name='results'):

    os.makedirs(folder_name, exist_ok=True) # Create the folder if it doesn't exist
    plt.figure(figsize=(8, 6)) # Set the figure size
    sns.set_context("paper", font_scale=1.2) 
    sns.set_style("ticks") # Set the style of the plot

    for d, x, y, slope, intercept, marker, color in zip(distances, x_data, y_data, slopes, intercepts, markers, colors):
        X = np.array(np.log(x)) # Convert the list to a numpy array
        Y = np.array(np.log(y)) 
        plt.scatter(X, Y, label=f'd={d} cm', marker=marker, color=color) # Scatter plot of the data points

        X_full_range = np.linspace(min(X) - 0.025*max(X), max(X) + 0.025*max(X), 100) # Create a range of x values for the fitted line
        plt.plot(X_full_range, slope * X_full_range + intercept, color=color) # Plot the fitted line

    plt.xlabel(r"$\ln(T)$") # X-axis label
    plt.ylabel(r"$\ln(P)$") # Y-axis label
    plt.title(r'Figure 2: Linear Regression ($\ln(T)$ vs $\ln(P)$) for Different Distances') # Title of the plot
    plt.legend(frameon=True, edgecolor="gray") # Show legend
    #sns.despine() # Remove the top and right spines of the plot
    
    #plt.show() 
    file_path = os.path.join(folder_name, f"grouped_linear_regression_plot_stef-bolt.pdf")
    plt.savefig(file_path, dpi=300, bbox_inches='tight') # Save the plot as a PDF file
    plt.close() # Close the plot to free memory


def get_temp(voltage, current):
    t_0 = 300 # Reference temperature in Kelvin
    r_0 = 0.5 # Reference resistance in Ohms
    alpha = 4.5e-3 # Temperature coefficient of resistance in 1/K
    resistance = voltage / current
    temp = t_0 + (resistance - r_0)/(alpha * r_0)
    return temp

def relative_error(measured, true):
    error = (abs(measured - true)/true) * 100
    return error


def main():
    #Set the global configuration dor the plotting
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42
    plt.rcParams["axes.edgecolor"] = "black"  
    plt.rcParams["axes.linewidth"] = 1.2  
    plt.rcParams["xtick.color"] = "black"  
    plt.rcParams["ytick.color"] = "black" 
    plt.rcParams["xtick.top"] = True
    plt.rcParams["ytick.right"] = True
    plt.rcParams["xtick.direction"] = "in"
    plt.rcParams["ytick.direction"] = "in"

    markers = ["o", "s", "^", "D", "v"]  # Different markers for the plot
    colors = ["blue", "green", "orange", "red", "purple"]  # Different colors for the plot

    full_X_data = [] # List to store all the data
    full_Y_data = [] 
    slopes = [] # List to store the slopes
    intercepts = [] # List to store the intercepts


    fout = open("results/results.txt", "w") # Open a file to write the results
    fout.write("\t--- Stefan-Boltzmann experiment results: ---\n")

    for distance in np.linspace(2, 10, 5): # Loop over the distances from 2 to 10 cm
        file_name = f"{int(distance)}_cm.txt"
        points = read_values(file_name)

        # Getting the temperatures 
        v = points['V']
        i = points['I']
        temp = get_temp(v, i)
        full_X_data.append(temp) # Temperature for the x-axis

        # Getting the power
        mV = points['mV']
        power = mV/22 # From the relation 22 mV/mW
        full_Y_data.append(power) # Power for the y-axis

        slope, intercept, r_squared = linear_regression(np.log(temp), np.log(power))
        slopes.append(slope)
        intercepts.append(intercept)

        fout.write(f"\n--- Data for the distance {distance} cm ---\n")
        fout.write(f"\tSlope [Ln(T) -> Ln(P)]: {slope:.4f} \n\tIntercept: {intercept:.4f} \n\tR-squared: {r_squared:.4f}\n\tRelative error: {relative_error(slope, 4):.2f}%\n")

    fout.write(f"\n\t--- General Results ---\n")
    fout.write(f"\tMean Slope [Ln(T) -> Ln(P)]: {np.mean(slopes):.4f} \n\tRelative error: {relative_error(np.mean(slopes), 4):.2f}%\n")
    
    grouped_plot(np.linspace(2, 10, 5), full_X_data, full_Y_data, slopes, intercepts, markers, colors)

    fout.close() # Close the file
    print("Results were saved on results/results.txt")


if __name__ == "__main__":
    main()