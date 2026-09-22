import os 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from scipy import stats

def read_values(file_name):
    """
    sep: Means the separation between values, in this case, the space 
    header: Since we don´t have headers on the raw text file
    names: Manually written headers 
    """
    points = pd.read_csv(f"data/{file_name}", sep='\\s+', header=None, names=['Temp', 'Mass'])
    return points 

def linear_regression(x, y):
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

def plot_data(figure_number, metal, temps, masses, slopes, intercepts, initial_temp, last_temp, folder_name='results'):

    os.makedirs(folder_name, exist_ok=True) # Create the folder if it doesn't exist

    plt.figure(figsize=(10, 6))

    sns.set_context("paper", font_scale=1.2) 
    sns.set_style("ticks") # Set the style of the plot

    temps = np.array(temps) # Convert the list to a numpy array
    masses = np.array(masses)
    plt.scatter(temps, masses, marker='o', color='b')

    x_full_range = np.linspace(initial_temp, last_temp, 100) # Create a range of x values for the fitted line

    for slope, intercept in zip(slopes, intercepts):
        plt.plot(x_full_range, slope * x_full_range + intercept, color='r') # Plot the fitted line

    plt.title(f'Figure {figure_number}: Data Points for {metal.capitalize()}', fontsize=14)
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Mass (g)')
    #plt.grid(True)
    #plt.legend(frameon=True, edgecolor="gray") # Show legend
    #sns.despine() # Remove the top and right spines of the plot
    
    #plt.show() # Show the plot
    file_path = os.path.join(folder_name, f'{metal}_spectrum.pdf')
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

    folder_name = 'results'
    figure_numbers = [6, 7] # Figure numbers for the plots
    metals = ['copper', 'zinc']
    mass_whenTis0 = [1625.12, 1509.2] # Mass of the system when the metal's temperature is 0°C  (or lower)

    for number, metal, mass_on0 in zip(figure_numbers, metals, mass_whenTis0):
        file_name = f"heated_{metal}.txt"
        points = read_values(file_name)
        temps = points['Temp']
        masses = points['Mass']

        mask = (temps >= 0) & (masses > mass_on0) # Condition to separate the data 
        temps_1 = temps[mask]
        masses_1 = masses[mask]
        temps_2 = temps[~mask]
        masses_2 = masses[~mask]

        slope_1, intercept_1, _ = linear_regression(temps_1, masses_1)
        slope_2, intercept_2, _ = linear_regression(temps_2, masses_2)
        slopes = [slope_1, slope_2]
        intercepts = [intercept_1, intercept_2]

        plot_data(number, metal, temps, masses, slopes, intercepts, min(temps), max(temps), folder_name)
        print(f"Data points for {metal.capitalize()} have been plotted and saved in the '{folder_name}' folder.")

if __name__ == "__main__":
    main()