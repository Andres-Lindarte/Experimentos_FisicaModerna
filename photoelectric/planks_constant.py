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
    points = pd.read_csv(f"data/{file_name}", sep='\\s+', header=None, names=['V', 'I'])
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

    plt.xlabel("Frequency (Hz)") # X-axis label
    plt.ylabel("Maximum Kinetic Energy (eV)") # Y-axis label
    plt.title(f'Frequency (Hz) vs Maximum Kinetic Energy (eV)') # Title of the plot
    #plt.legend(frameon=True, edgecolor="gray") # Show legend
    #sns.despine() # Remove the top and right spines of the plot
    
    #plt.show() 
    file_path = os.path.join(folder_name, f"planks_constant_linear_regression_plot.pdf")
    plt.savefig(file_path, dpi=300, bbox_inches='tight') # Save the plot as a PDF file
    plt.close() # Close the plot to free memory


def grouped_plot(wave_lengths, x_data, y_data, slopes, intercepts, markers, colors, folder_name='results'):

    os.makedirs(folder_name, exist_ok=True) # Create the folder if it doesn't exist
    plt.figure(figsize=(8, 6)) # Set the figure size
    sns.set_context("paper", font_scale=1.2) 
    sns.set_style("ticks") # Set the style of the plot

    for wl, x, y, slope, intercept, marker, color in zip(wave_lengths, x_data, y_data, slopes, intercepts, markers, colors):
        X = np.array(x) # Convert the list to a numpy array
        Y = np.array(y) 
        plt.scatter(X, Y, label=f'Data points (λ={wl} nm)', marker=marker, color=color) # Scatter plot of the data points
        
        max_y = np.max(Y)
        y_end = max_y * 1.05
        Y_line = np.array([0, y_end])
        X_line = (Y_line - intercept) / slope # Calculate the x values for the fitted line
        plt.plot(X_line, Y_line, label=f'Fitted line (λ={wl} nm)', color=color) # Plot the fitted line

    plt.xlabel("Voltage (V)") # X-axis label
    plt.ylabel("Current (A)") # Y-axis label
    plt.title('Figure 2: Linear Regression for Different Wavelengths') # Title of the plot
    plt.legend(frameon=True, edgecolor="gray") # Show legend
    #sns.despine() # Remove the top and right spines of the plot
    
    #plt.show() 
    file_path = os.path.join(folder_name, f"grouped_linear_regression_plot_photo.pdf")
    plt.savefig(file_path, dpi=300, bbox_inches='tight') # Save the plot as a PDF file
    plt.close() # Close the plot to free memory

def fix_data_by_eye(x, y, increasing_points, tolerance=1.0):
    mask_null = np.abs(np.array(y)) < tolerance # Mask for points close to zero
    mask_slope = np.array(x) > increasing_points

    x_null = x[mask_null]
    y_null = y[mask_null] # Get the points close to zero
    mean_null = np.mean(y_null)
    x_fixed = x
    y_fixed = y - mean_null # Subtract the mean of the points close to zero from all points

    x_slope = x_fixed[mask_slope]
    y_slope = y_fixed[mask_slope] 

    return x_fixed, y_fixed, x_slope, y_slope


def fix_data_by_porcentage(x, y, increasing_points, tolerance=1.0, lower_percentage=0.03, upper_percentage=0.20):
    mask_null = np.abs(np.array(y)) < tolerance # Mask for points close to zero

    # Mask for the increasing points based on the percentage of the maximum value
    max_y = np.max(np.abs(y))
    lower_bound = lower_percentage * max_y
    upper_bound = upper_percentage * max_y
    mask_slope = (np.abs(y) >= lower_bound) & (np.abs(y) <= upper_bound)

    x_null = x[mask_null]
    y_null = y[mask_null] # Get the points close to zero
    mean_null = np.mean(y_null)
    x_fixed = x
    y_fixed = y - mean_null # Subtract the mean of the points close to zero from all points

    x_slope = x_fixed[mask_slope]
    y_slope = y_fixed[mask_slope] 

    return x_fixed, y_fixed, x_slope, y_slope


def get_max_K(slope, intercept): # Get the maximum kinetic energy from the slope and intercept of the linear regression
    return -intercept/slope

def calculate_h_and_w(max_k, wave_length): # Calculate Planck's constant and the work function 
    e_charge=1.602e-19
    frequency = 3e8/(np.array(wave_length)*1e-9) # Calculate the frequency from the wavelength
    h_over_e, w_over_e, _ = linear_regression(frequency, np.abs(max_k))
    h = h_over_e * e_charge
    w = -w_over_e * e_charge
    return frequency, h_over_e, w_over_e, h, w

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

    wave_lengths = [365, 405, 436, 546, 578] # Wavelengths in nm 
    markers = ["o", "s", "^", "D", "v"]  # Different markers for each wavelength
    colors = ["blue", "green", "orange", "red", "purple"]  # Different colors for each wavelength
    #increasing_points = [-1.6, -1.02, -0.71, -0.48, -0.24] # Points where the data is increasing
    increasing_points = [-1.71, -1.25, -0.89, -0.61, -0.4] # Points where the data is increasing
    full_X_data = [] # List to store all the data
    full_Y_data = [] 
    slopes = [] # List to store the slopes
    intercepts = [] # List to store the intercepts
    max_energies = [] # List to store the maximum kinetic energies


    fout = open("results/results.txt", "w") # Open a file to write the results
    fout.write("\t--- Photoelectric experiment results: ---\n")

    for wl, inc_point in zip(wave_lengths, increasing_points):
        file_name = f"{wl}.txt"
        data = read_values(file_name)
        x = data['V']
        y = data['I']

        #x_fixed, y_fixed, x_slope, y_slope = fix_data_by_eye(x, y, inc_point)
        x_fixed, y_fixed, x_slope, y_slope = fix_data_by_porcentage(x, y, inc_point)
        full_X_data.append(x_fixed)
        full_Y_data.append(y_fixed)
        
        slope, intercept, r_squared = linear_regression(x_slope, y_slope)
        slopes.append(slope)
        intercepts.append(intercept)
        max_K = get_max_K(slope, intercept)
        max_energies.append(max_K)

        fout.write(f"\n--- Data for {file_name} nm ---\n")
        fout.write(f"\tSlope: {slope:.4f} \n\tIntercept: {intercept:.4f} \n\tMaximum kinetic energy (eV): {np.abs(max_K):.4f} \n\tR-squared: {r_squared:.4f}\n")
        
    grouped_plot(wave_lengths, full_X_data, full_Y_data, slopes, intercepts, markers, colors)
    frequencies, h_slope, w_slope, h, w = calculate_h_and_w(max_energies, wave_lengths)
    individual_plot(frequencies, np.abs(max_energies), h_slope, w_slope)
    fout.write(f"\n\t--- Planck's constant and work function ---\n")
    fout.write(f"\tExperimental Planck's constant (h): {h:.4e} J·s\n\tExperimental Work function (w): {w:.4e} J\n")
    fout.write(f"\tRelative error for Planck's constant: {relative_error(h, 6.626e-34):.2f}%\n")
    fout.write(f"\tRelative error for work function: {relative_error(w, 2.28e-19):.2f}%\n")

    fout.close() # Close the file
    print("Results were saved on results/results.txt")


if __name__ == "__main__":
    main()