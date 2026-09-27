import os 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from scipy import stats
from scipy import constants

def read_values(file_name: str):
    """
    sep: Means the separation between values, in this case, the space 
    header: Since we don´t have headers on the raw text file
    names: Manually written headers 
    """
    points = pd.read_csv(f"data/{file_name}", sep='\\s+')
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

def mean_2_values(low: float, high: float):
    return (low + high)/2

def calculate_sen_theta(diameter: float, long: float = 135):
    return np.sin(0.5*np.arctan(diameter/(2*long))) # Calculate the sen of angle theta in radians

def calculate_inverse_squared_eV(voltaje: float):
    return (1/np.sqrt(voltaje*1000))

def calculate_distance_from_slope(slope: float):
    h = 6.6262e-34 # Planck's constant in J*s
    m_e = 9.109e-31 # Electron mass in kg
    factor = 1/(np.sqrt(6.242e18)) # Conversion factor KeV to J
    distance = (h/(2*np.sqrt(2*m_e)*factor*slope)) # Calculate the distance from the slope using the de Broglie wavelength formula
    return distance 

def relative_error(measured, true):
    error = (abs(measured - true)/true) * 100
    return error

def grouped_plot(x_data: list, y_data: list, slopes: list, intercepts: list, figure_number: int = 2, folder_name: str = 'results'):

    os.makedirs(folder_name, exist_ok=True) # Create the folder if it doesn't exist

    plt.figure(figsize=(8, 6)) # Set the figure size

    sns.set_context("paper", font_scale=1.2) 
    sns.set_style("ticks") # Set the style of the plot

    for x, y, slope, intercept in zip(x_data, y_data, slopes, intercepts):
        X = np.array(x) # Convert the list to a numpy array
        Y = np.array(y) 
        plt.scatter(X, Y) # Scatter plot of the data points
        X_full_range = np.linspace(min(X), max(X), 100) # Create a range of x values for the fitted line
        plt.plot(X_full_range, slope * X_full_range + intercept) # Plot the fitted line

    plt.xlabel(r"$\frac{1}{\sqrt{eV}} [au]$") # X-axis label
    plt.ylabel(r"$\sin(\theta) [au]$") # Y-axis label
    plt.title(f'Figure {figure_number}: ' + r'$\sin(\theta)$ vs $\frac{1}{\sqrt{eV}}$') # Title of the plot
    #plt.legend(frameon=True, edgecolor="gray") # Show legend
    #sns.despine() # Remove the top and right spines of the plot
    
    #plt.show() 
    file_path = os.path.join(folder_name, f"distance_results.pdf")
    plt.savefig(file_path, dpi=300, bbox_inches='tight') # Save the plot as a PDF file
    plt.close() # Close the plot to free memory

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

    real_distances = [2.13e-10, 1.23e-10]

    fout = open("results/results.txt", "w") # Open a file to write the results
    fout.write("\t--- Calorific Capacity Results: ---\n")

    X_total = []
    Y_total = []
    slopes = []
    intercepts = []
    for ii in range(1, 3):
        x_data = []
        y_data = []
        file_name = f"d_{ii}.txt"
        points = read_values(file_name)
        fout.write(f"\n--- Data from {file_name} ---\n")
        fout.write(f"Voltage (V): {(points['potential'].values)*1000}\n")
        fout.write(f"Internal Diameter (mm): {points['internal'].values}\n")
        fout.write(f"External Diameter (mm): {points['external'].values}\n")

        X_data = calculate_inverse_squared_eV(points['potential'])
        X_total.append(X_data)

        diameter_mean = mean_2_values(points['internal'], points['external'])
        fout.write(f"Mean Diameter (mm): {diameter_mean.values}\n")
        Y_data = calculate_sen_theta(diameter_mean)
        Y_total.append(Y_data)

        slope, intercept, _ = linear_regression(X_data, Y_data)
        slopes.append(slope)
        intercepts.append(intercept)

        distance = calculate_distance_from_slope(slope)
        rel_error = relative_error(distance, real_distances[ii-1])
        fout.write("\n\tRESULTS: \n")
        fout.write(f"Slope: {slope}\n")
        fout.write(f"Intercept: {intercept}\n")
        fout.write(f"Distance (D_{ii}): {distance}\n")
        fout.write(f"Real distance: {real_distances[ii-1]}\n")
        fout.write(f"Relative error: {rel_error}%\n")
    
    grouped_plot(X_total, Y_total, slopes, intercepts)

    print("Results were saved on results/results.txt")


if __name__ == "__main__":
    main()
