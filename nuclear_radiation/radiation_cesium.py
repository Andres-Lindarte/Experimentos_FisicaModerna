import os 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from scipy import stats

def read_values(file_name: str, header_1: str, header_2: str):
    """
    sep: Means the separation between values, in this case, the space 
    header: Since we don´t have headers on the raw text file
    names: Manually written headers 
    """
    points = pd.read_csv(f"data/{file_name}", sep='\\s+', header=None, names=[header_1, header_2])
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

    # Part 1: Caracterization of the devise
    file_name = "radiation_vs_voltage_data.txt"
    points = read_values(file_name, 'V', 'Rad')
    v = points['V']
    r = points['Rad']
    individual_plot(v, r, "Voltage (V)", "Radiation ()", "Radiation vs Voltage", "devise_caracterization.pdf", lines=True)
    
    # Part 2: Changing the distance 
    file_name_2 = "radiation_vs_distance.txt"
    points_2 = read_values(file_name_2, 'Rad', 'None')
    d = np.arange(1, 11, 1) # Distances from 1 to 10 cm
    r_2_raw = points_2['Rad']
    r_2 = []
    r_2_log = []
    for ii in range(10): # Select the mean of every 4 points to get the average radiation at each distance
        start = 4*ii
        end = start + 4
        r_2.append(np.mean(r_2_raw[start:end]))
        r_2_log.append(np.mean(np.log(r_2_raw[start:end])))
    slope, intercept, r_squared = linear_regression(np.log(d), r_2_log)
    individual_plot(d, r_2, "Distance (cm)", "Radiation ()", "Radiation vs Distance", "radiation_vs_distance.pdf")
    individual_plot(np.log(d), r_2_log, "Log Distance (cm)", "Log Radiation", "Log Radiation  vs Log Distance", "log_radiation_vs_log_distance.pdf", slope=slope, intercept=intercept)
    fout = open("results/results_distance.txt", "w") # Open a file to write the results
    fout.write("\t--- 'Radiation vs distance' results: ---\n")
    fout.write(f"Slope (log(Rad) vs log(d)): {slope}\n")
    fout .write(f"Intercept (log(Rad) vs log(d)): {intercept}\n")
    fout.write(f"R-squared (log(Rad) vs log(d)): {r_squared}\n")
    fout.close() # Close the file

    # Part 3: 
    file_name_3 = "radiation_vs_distance.txt"
    points_3 = read_values(file_name_3, 'Rad', 'None')
    thickness = [5e-4, 11e-4, 17.6e-4, 32.1e-4, 43.35e-4, 66.85e-4]
    r_3_raw = points_3['Rad']
    r_3 = []
    r_3_log = []
    for ii in range(len(thickness)): # Select the mean of every 4 points to get the average radiation at each thickness
        start = 4*ii
        end = start + 4
        r_3.append(np.mean(r_3_raw[start:end]))
        r_3_log.append(np.mean(np.log(r_3_raw[start:end])))
    slope, intercept, r_squared = linear_regression(thickness, r_3_log)
    individual_plot(thickness, r_3, "Thickness (m)", "Radiation ()", "Radiation vs Thickness", "radiation_vs_thickness.pdf")
    individual_plot(thickness, r_3_log, "Thickness (m)", "Log Radiation", "Log Radiation  vs Thickness", "log_radiation_vs_thickness.pdf", slope=slope, intercept=intercept)
    fout = open("results/results_thickness.txt", "w") # Open a file to write the results
    fout.write("\t--- 'Radiation vs thickness' results: ---\n")
    fout.write(f"Slope (log(Rad) vs thickness): {slope}\n")
    #fout.write(f"Relative error (slope): {relative_error(slope, -19.5)}%\n")
    fout .write(f"Intercept (log(Rad) vs thickness): {intercept}\n")
    fout.write(f"R-squared (log(Rad) vs thickness): {r_squared}\n")
    fout.close() # Close the file

    print("Results were saved on the results folder")


if __name__ == "__main__":
    main()