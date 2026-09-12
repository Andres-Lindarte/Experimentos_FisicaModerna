import os 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def get_data(file_name):
    # Reads data from a text file and returns it as a numpy array
    return np.loadtxt(f"data/{file_name}")

def plot_data(wave_length, points, folder_name='results'):

    os.makedirs(folder_name, exist_ok=True) # Create the folder if it doesn't exist

    plt.figure(figsize=(10, 6))

    sns.set_context("paper", font_scale=1.2) 
    sns.set_style("ticks") # Set the style of the plot

    plt.plot(wave_length, points, marker='o', linestyle='-', color='b')
    plt.title('Data Points')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Radiance (W/m^2/nm)')
    #plt.grid(True)
    plt.legend(frameon=True, edgecolor="gray") # Show legend
    #sns.despine() # Remove the top and right spines of the plot
    
    #plt.show() # Show the plot
    file_path = os.path.join(folder_name, 'spectrum.pdf')
    plt.savefig(file_path, dpi=300, bbox_inches='tight') # Save the plot as a PDF file
    plt.close() # Close the plot to free memory


def main():
    file_name = 't_1.txt'
    folder_name = 'results'
    
    # 161 point s from 200 to 1000 nm with a step of 5 nm
    wave_length = np.arange(200, 1005 , 5)
    
    points = get_data(file_name)

    # Validate the length of wave_length and points
    if len(wave_length) != len(points):
        print(f"Attention: X has {len(wave_length)} values but the file has {len(points)} rows.")
        return

    plot_data(wave_length, points, folder_name)

if __name__ == "__main__":
    main()