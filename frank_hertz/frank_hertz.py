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


def grouped_plot(variation_name, variation, x_data, y_data, x_label, y_label, title, markers, colors, file_name, folder_name='results'):

    os.makedirs(folder_name, exist_ok=True) # Create the folder if it doesn't exist
    plt.figure(figsize=(8, 6)) # Set the figure size
    sns.set_context("paper", font_scale=1.2) 
    sns.set_style("ticks") # Set the style of the plot

    if variation_name == "voltages":
        label, units = "V", "kV"
    elif variation_name == "temperatures":
        label, units = "T", "K"
    else:
        label, units = "Variation", ""

    for var, x, y, color in zip(variation, x_data, y_data, colors):
        X = np.array(x) # Convert the list to a numpy array
        Y = np.array(y) 
        plt.plot(X, Y, label=f'{label} = {var} {units}', color=color) # Scatter plot of the data points

    plt.xlabel(x_label) # X-axis label
    plt.ylabel(y_label) # Y-axis label
    plt.title(title) # Title of the plot
    plt.legend(frameon=True, edgecolor="gray") # Show legend
    #sns.despine() # Remove the top and right spines of the plot
    
    #plt.show() 
    file_path = os.path.join(folder_name, f"{file_name}.pdf")
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


    # --- Part 1 ---
    temps = [162, 173, 180, 189, 199]
    full_X_data = []
    full_Y_data = []

    for temp in temps:
        data = read_values(f"v1.8_t{temp}_data.txt")
        full_X_data.append(data['V'])
        full_Y_data.append(data['I'])

    grouped_plot("temperatures", temps, full_X_data, full_Y_data, "Voltage (V)", "Current (A)", "Figure 2: Current vs Voltage for different temperatures", markers=['o', 's', '^', 'D', 'v'], colors=['blue', 'orange', 'green', 'red', 'purple'], file_name="grouped_plot_temperature")

    # --- Part 2 ---
    names = ["1.8_t180", "2.0_t182", "2.2_t182", "2.35_t182"]
    full_X_data_2 = []
    full_Y_data_2 = []

    for name in names:
        data = read_values(f"v{name}_data.txt")
        full_X_data_2.append(data['V'])
        full_Y_data_2.append(data['I'])

    grouped_plot("voltages", [1.8, 2.0, 2.2, 2.35], full_X_data_2, full_Y_data_2, "Voltage (V)", "Current (A)", "Figure 3: Current vs Voltage for different voltages", markers=['o', 's', '^', 'D'], colors=['blue', 'orange', 'green', 'red'], file_name="grouped_plot_voltage")

    print("Results were saved in the results folder")

if __name__ == "__main__":
    main()