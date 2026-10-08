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


def grouped_plot(ii, wave_length, x_data, y_data, markers, colors, folder_name='results'):

    os.makedirs(folder_name, exist_ok=True) # Create the folder if it doesn't exist

    plt.figure(figsize=(8, 6)) # Set the figure size

    sns.set_context("paper", font_scale=1.2) 
    sns.set_style("ticks") # Set the style of the plot

    for x, y, marker, color in zip(x_data, y_data, markers, colors):
        X = np.array(x) # Convert the list to a numpy array
        Y = np.array(y) 
        plt.scatter(X, Y, label=f'Intesity {1+ii}', marker=marker, color=color) # Scatter plot of the data points

    plt.xlabel("Voltage (V)") # X-axis label
    plt.ylabel("Current (A)") # Y-axis label
    plt.title(f'Figure {4+ii}: Diferent intesities for λ={wave_length} nm') # Title of the plot
    plt.legend(frameon=True, edgecolor="gray") # Show legend
    #sns.despine() # Remove the top and right spines of the plot
    
    #plt.show() 
    file_path = os.path.join(folder_name, f"{wave_length}_intensities.pdf")
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

    wave_lengths = [365, 405, 546, 578] # Wavelengths in nm 
    markers = ["o", "s", "^", "D"]  # Different markers for each wavelength
    colors = ["blue", "green", "orange", "red"]  # Different colors for each wavelength

    for wl in wave_lengths:
        x_data = [] # List to store the x data for each wavelength
        y_data = [] # List to store the y data for each wavelength
        for intensity in range(1, 5):
            file_name = f"{intensity}_{wl}.txt"
            data = read_values(file_name)
            x = data['V']
            y = data['I']

            x_data.append(x)
            y_data.append(y)
        
        grouped_plot(wave_lengths.index(wl), wl, x_data, y_data, markers, colors)

    print("Results were saved on results/results.txt")

if __name__ == "__main__":
    main()