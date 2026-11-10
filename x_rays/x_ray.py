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
    points = pd.read_csv(f"data/{file_name}", sep='\\s+', header=None, names=['Angle', '1', '2', '3', '4', '5', '6'])
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


def individual_plot(x, y, xlable: str, ylable: str, title: str, image_name: str, lines=False, slope=None, intercept=None, folder_name='results'):

    os.makedirs(folder_name, exist_ok=True) # Create the folder if it doesn't exist

    X = np.array(x) # Convert the list to a numpy array
    Y = np.array(y) 

    plt.figure(figsize=(8, 6)) # Set the figure size

    sns.set_context("paper", font_scale=1.2) 
    sns.set_style("ticks") # Set the style of the plot

    plt.scatter(X, Y, color='blue') # Scatter plot of the data points
    if lines: # Plot the lines if needed
        plt.plot(X, Y, color='blue', linestyle='--') 

    if slope is not None:
        plt.plot(X, slope * X + intercept, color='red') # Plot the fitted line

    plt.xlabel(xlable) # X-axis label
    plt.ylabel(ylable) # Y-axis label
    plt.title(title) # Title of the plot
    #plt.legend(frameon=True, edgecolor="gray") # Show legend
    #sns.despine() # Remove the top and right spines of the plot
    
    #plt.show() 
    file_path = os.path.join(folder_name, image_name)
    plt.savefig(file_path, dpi=300, bbox_inches='tight') # Save the plot as a PDF file
    plt.close() # Close the plot to free memory


def grouped_plot(variation_name, variation, x_data, y_data, x_label, y_label, title, markers, colors, file_name, folder_name='results'):

    os.makedirs(folder_name, exist_ok=True) # Create the folder if it doesn't exist
    plt.figure(figsize=(8, 6)) # Set the figure size
    sns.set_context("paper", font_scale=1.2) 
    sns.set_style("ticks") # Set the style of the plot

    if variation_name == "voltages":
        label, units = "V", "kV"
    elif variation_name == "currents":
        label, units = "I", "A"
    else:
        label, units = "Variation", ""

    X = np.array(x_data) # Convert the list to a numpy array
    for var, y, marker, color in zip(variation, y_data, markers, colors):
        Y = np.array(y) 
        plt.plot(X, Y, label=f'{label} = {var} {units}', marker=marker, linestyle= '-', color=color) # Scatter plot of the data points

    plt.xlabel(x_label) # X-axis label
    plt.ylabel(y_label) # Y-axis label
    plt.title(title) # Title of the plot
    plt.legend(frameon=True, edgecolor="gray") # Show legend
    #sns.despine() # Remove the top and right spines of the plot
    
    #plt.show() 
    file_path = os.path.join(folder_name, f"{file_name}.pdf")
    plt.savefig(file_path, dpi=300, bbox_inches='tight') # Save the plot as a PDF file
    plt.close() # Close the plot to free memory


def bragg(theta: float, n: int = 1, d: float = 282e-12):
    """
    Calculate the wavelength using Bragg's law.
    theta: Angle in degrees
    n: Order of diffraction (default is 1)
    d: Spacing between planes in meters (default is 282 pm)
    """
    theta_rad = np.radians(theta)  # Convert angle to radians
    wavelength = (2 * d * np.sin(theta_rad)) / n  # Bragg's law formula
    return wavelength * 1e9  # Return wavelength in nanometers


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

    voltages = [20, 22, 24, 26, 28, 30] # Voltages in Kv
    markers = ["o", "s", "^", "D", "v", "*"]  # Different markers for each voltage
    colors = ["blue", "green", "orange", "red", "purple", "black"]  # Different colors for each voltage

    # --- Part 1: ---
    fout = open("results/results_voltage.txt", "w") # Open a file to write the results
    fout.write("\t--- X-Ray experiment results: ---\n")

    data = read_values("change_voltage_data.txt")
    X_data = data['Angle']  # X-axis data (Angle)
    Y_data = [data[str(ii)] for ii in range(1, 7)]  # Y-axis data (Intensities)

    grouped_plot("voltages", voltages, X_data, Y_data, "Angle (°)", "Intensity (a.u.)", "Intensity vs Angle for different voltages", markers, colors, "grouped_intensity_plot_XRay_voltage")
    # The degrees were given by eye
    fout.write("Frist order results (given by the Bragg's law) n=1 and d=282 pm:\n")
    fout.write(f"\tK_alpha was fount at 6.4° (aprox); lamba = {bragg(6.4, n=1, d=282e-12):.2e} nm\n")
    fout.write(f"\tK_betha was fount at 7.3° (aprox); lamba = {bragg(7.3, n=1, d=282e-12):.2e} nm\n")

    # Min degrees (the ones that are the closest to the x-axis) were given by eye
    min_degrees = [5.7, 5.1, 4.7, 4.2, 3.9, 3.5]
    min_wavelengths = [bragg(theta, n=1, d=282e-12) for theta in min_degrees] 
    inv_volt = [1/(v*1000) for v in voltages]
    slope, intercept, r_squared = linear_regression(inv_volt, min_wavelengths)
    individual_plot(inv_volt, min_wavelengths, "1/Voltage (1/V)", "Wavelength (nm)", "Wavelength vs 1/Voltage", "wavelength_vs_1_over_voltage.pdf", slope=slope, intercept=intercept)
    fout.write("\nWavelength vs 1/Voltage to calculate the Plank's constant:\n")
    fout.write(f"\tSlope = {slope:.2e} m*V\n")
    fout.write(f"\tIntercept = {intercept:.2e} m\n")
    fout.write(f"\tR-squared = {r_squared}\n")
    C = 3e8  # Speed of light in m/s
    E = 1.602e-19  # Charge of the electron in Coulombs
    h = slope * 1e-9 * E / C  # Calculate Planck's constant in J*s
    fout.write(f"\tPlank's constant = {h:.2e} J*s; Relative error = {relative_error(h, 6.626e-34):.2f}%\n")
    fout.close()


    # --- Part 2: ---
    currents = [1, 2, 3, 4] # Currents in amps    
    markers_2 = ["^", "D", "v", "*"]  # Different markers for each voltage  
    colors_2 = ["blue", "green", "orange", "red"]  # Different colors for each voltage
    data_2 = read_values("change_current_data.txt")
    Y_data_2 = [data_2[str(ii)] for ii in range(1, 5)]  # Y-axis data (Intensities)
    
    grouped_plot("currents", currents, X_data, Y_data_2, "Angle (°)", "Intensity (a.u.)", "Intensity vs Angle for different currents", markers_2, colors_2, "grouped_intensity_plot_XRay_current")

    print("Results were saved in the results folder")

if __name__ == "__main__":
    main()