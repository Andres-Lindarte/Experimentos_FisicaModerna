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


def grouped_plot(voltages, x_data, y_data, markers, colors, folder_name='results'):

    os.makedirs(folder_name, exist_ok=True) # Create the folder if it doesn't exist
    plt.figure(figsize=(8, 6)) # Set the figure size
    sns.set_context("paper", font_scale=1.2) 
    sns.set_style("ticks") # Set the style of the plot

    for wl, x, y, slope, intercept, marker, color in zip(x_data, y_data, markers, colors):
        X = np.array(x) # Convert the list to a numpy array
        Y = np.array(y) 
        plt.scatter(X, Y, label=f'Data points (λ={wl} nm)', marker=marker, color=color) # Scatter plot of the data points

    plt.xlabel("Angle (degree))") # X-axis label
    plt.ylabel("Intensity ()") # Y-axis label
    plt.title('Figure 2: Intensity vs difraction angle') # Title of the plot
    plt.legend(frameon=True, edgecolor="gray") # Show legend
    #sns.despine() # Remove the top and right spines of the plot
    
    #plt.show() 
    file_path = os.path.join(folder_name, f"grouped_intensity_plot_XRay_voltage.pdf")
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

    voltages = [20, 22, 24, 26, 28, 30] # Voltages in V 
    markers = ["o--", "s--", "^--", "D--", "v--", "*--"]  # Different markers for each voltage
    colors = ["blue", "green", "orange", "red", "purple", "black"]  # Different colors for each voltage

    fout = open("results/results_voltage.txt", "w") # Open a file to write the results
    fout.write("\t--- X-Ray experiment results: ---\n")

    data = read_values()


if __name__ == "__main__":
    main()