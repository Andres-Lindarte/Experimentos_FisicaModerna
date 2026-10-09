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
    points = pd.read_csv(f"data/{file_name}", sep='\\s+', header=None, names=['D', 'mV'])
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

def individual_plot(x, y, slope, intercept, folder_name='results'):

    os.makedirs(folder_name, exist_ok=True) # Create the folder if it doesn't exist

    X = np.array(x) # Convert the list to a numpy array
    Y = np.array(y) 

    plt.figure(figsize=(8, 6)) # Set the figure size

    sns.set_context("paper", font_scale=1.2) 
    sns.set_style("ticks") # Set the style of the plot

    plt.scatter(X, Y, color='blue') # Scatter plot of the data points
    plt.plot(X, slope * X + intercept, color='red') # Plot the fitted line

    plt.xlabel("Ln of Distances (m)") # X-axis label
    plt.ylabel("Ln of the power (W)") # Y-axis label
    plt.title(f'Ln of Distances (m) vs Ln of the power (W)') # Title of the plot
    #plt.legend(frameon=True, edgecolor="gray") # Show legend
    #sns.despine() # Remove the top and right spines of the plot
    
    #plt.show() 
    file_path = os.path.join(folder_name, f"distance_variation_radiation.pdf")
    plt.savefig(file_path, dpi=300, bbox_inches='tight') # Save the plot as a PDF file
    plt.close() # Close the plot to free memory


def relative_error(measured, true):
    error = (abs(measured - true)/abs(true)) * 100
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

    fout = open("results/results_distance.txt", "w") # Open a file to write the results
    fout.write("\t--- Stefan-Boltzmann experiment results (variating the distance)- 6.9 V - 1.32 A: ---\n")

    file_name = f"distance_variation.txt"
    points = read_values(file_name)

    # Getting the distances 
    d = points['D'] * 1e-2 # Convert from cm to m
    
    # Getting the power
    mV = points['mV']
    power = mV/22 # From the relation 22 mV/mW

    slope, intercept, r_squared = linear_regression(np.log(d), np.log(power))
    fout.write(f"\tSlope [Ln(D) -> Ln(P)]: {slope:.4f} \n\tIntercept: {intercept:.4f} \n\tR-squared: {r_squared:.4f}\n\tRelative error: {relative_error(slope, -2):.2f}%\n")
    
    individual_plot(np.log(d), np.log(power), slope, intercept)

    fout.close() # Close the file
    print("Results were saved on results/results_distance.txt")


if __name__ == "__main__":
    main()