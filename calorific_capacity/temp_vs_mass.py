import os 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def read_values(file_name):
    """
    sep: Means the separation between values, in this case, the space 
    header: Since we don´t have headers on the raw text file
    names: Manually written headers 
    """
    points = pd.read_csv(f"data/{file_name}", sep='\\s+', header=None, names=['Temp', 'Mass'])
    return points 

def plot_data(temps, masses, folder_name='results'):

    os.makedirs(folder_name, exist_ok=True) # Create the folder if it doesn't exist

    plt.figure(figsize=(10, 6))

    sns.set_context("paper", font_scale=1.2) 
    sns.set_style("ticks") # Set the style of the plot

    plt.plot(temps, masses, marker='o', color='b')
    plt.title('Figure 2: Data Points', fontsize=14)
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Mass (g)')
    #plt.grid(True)
    plt.legend(frameon=True, edgecolor="gray") # Show legend
    #sns.despine() # Remove the top and right spines of the plot
    
    #plt.show() # Show the plot
    file_path = os.path.join(folder_name, 'spectrum.pdf')
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

    file_name = 'heated_copper.txt'
    folder_name = 'results'
    
    points = read_values(file_name)
    temps = points['Temp']
    masses = points['Mass']

    # Validate the length of temps and masses
    if len(temps) != len(masses):
        print(f"Attention: X has {len(temps)} values but the file has {len(masses)} rows.")
        return

    plot_data(temps, masses, folder_name)

if __name__ == "__main__":
    main()