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
    points = pd.read_csv(f"data/{file_name}", sep='\\s+', header=None, names=['V', 'R'])
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

def individual_plot(x, y, folder_name='results'):

    os.makedirs(folder_name, exist_ok=True) # Create the folder if it doesn't exist

    X = np.array(x) # Convert the list to a numpy array
    Y = np.array(y) 

    plt.figure(figsize=(8, 6)) # Set the figure size

    sns.set_context("paper", font_scale=1.2) 
    sns.set_style("ticks") # Set the style of the plot

    plt.scatter(X, Y, color='blue') # Scatter plot of the data points

    plt.xlabel("Inverse of the temperature (1/K)") # X-axis label
    plt.ylabel("Conductivity (S/m)") # Y-axis label
    plt.title(f'Figure 2:Conductivity (S/m) vs Inverse of the temperature (1/K)') # Title of the plot
    #plt.legend(frameon=True, edgecolor="gray") # Show legend
    #sns.despine() # Remove the top and right spines of the plot
    
    #plt.show() 
    file_path = os.path.join(folder_name, f"conductivity_inverse_temperature.pdf")
    plt.savefig(file_path, dpi=300, bbox_inches='tight') # Save the plot as a PDF file
    plt.close() # Close the plot to free memory

def fixed_plot(x, y, mask, slope, intercept, folder_name='results'):

    os.makedirs(folder_name, exist_ok=True) # Create the folder if it doesn't exist

    X = np.array(x) # Convert the list to a numpy array
    Y = np.array(y) 

    plt.figure(figsize=(8, 6)) # Set the figure size

    sns.set_context("paper", font_scale=1.2) 
    sns.set_style("ticks") # Set the style of the plot

    plt.scatter(X, Y, color='blue') # Scatter plot of the data points
    X_masked = X[mask]
    Y_masked = Y[mask]
    X_full_range = np.linspace(min(X_masked) - 0.025*max(X_masked), max(X_masked) + 0.025*max(X_masked), 100) # Create a range of x values for the fitted line
    plt.plot(X_full_range, slope * X_full_range + intercept, color='red') # Plot the fitted line

    plt.xlabel(r"$\frac{1}{T}$") # X-axis label
    plt.ylabel(r"$\ln(\sigma)$") # Y-axis label
    plt.title(r"Figure 3:$\ln(\sigma)$ vs $\frac{1}{T}$") # Title of the plot
    #plt.legend(frameon=True, edgecolor="gray") # Show legend
    #sns.despine() # Remove the top and right spines of the plot
    
    #plt.show() 
    file_path = os.path.join(folder_name, f"linear_regression_germanium.pdf")
    plt.savefig(file_path, dpi=300, bbox_inches='tight') # Save the plot as a PDF file
    plt.close() # Close the plot to free memory

def get_inverse_temp(voltage):
    t_0 = 300 # Room temperature in Kelvin
    constant = 10 # 10 mV/k devise indications
    temp = t_0 + voltage/constant
    return 1.0/temp

def get_conductivity(resistance):
    area_over_long = 0.5e-3
    resistivity = resistance*area_over_long
    return 1.0/resistivity

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

    fout = open("results/results.txt", "w") # Open a file to write the results
    fout.write("\t--- Stefan-Boltzmann experiment results: ---\n")

    file_name = f"germanium_data.txt"
    points = read_values(file_name)
    v = points['V']
    r = points['R']

    # Getting the temperatures 
    X_data = get_inverse_temp(v)
    # Getting the conductivity
    Y_data = get_conductivity(r)

    # Plot conductivity vs inverse temperature
    fout.write("\t--- Conductivity vs Inverse Temperature ---\n")
    fout.write("Inverse Temperature (1/K)\tConductivity (S/m)\n")
    for x, y in zip(X_data, Y_data):
        fout.write(f"{x:.6f}\t{y:.6f}\n")

    individual_plot(X_data, Y_data)

    Y_log = np.log(Y_data)
    slope, intercept, _ = linear_regression(X_data, Y_log)
    mask = (X_data > 0.0025) & (X_data < 0.0035) # TO-DO
    fixed_plot(X_data, Y_log, mask, slope, intercept)

    gap = slope*2.0*(8.617e-5) # Calculate the energy gap in eV using the slope and Boltzmann constant

    fout.write(f"\n\tGAP of energy of the germanium: {gap:.4f} eV \n\tRelative error: {relative_error(gap, 0.67):.2f}%\n")

    fout.close() # Close the file
    print("Results were saved on results/results.txt")


if __name__ == "__main__":
    main()