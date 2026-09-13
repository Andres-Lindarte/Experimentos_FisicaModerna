import os 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from scipy import stats

# Read the file 
def read_values(file_name):
    """
    sep: Means the separation between values, in this case, the space 
    header: Since we don´t have headers on the raw text file
    names: Manually written headers 
    """
    points = pd.read_csv(f"data/{file_name}", sep='\\s+', header=None, names=['Voltaje', 'Current', 'Value'])
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

def individual_plot(wl, x, y, slope, intercept, folder_name='results'):

    os.makedirs(folder_name, exist_ok=True) # Create the folder if it doesn't exist

    X = np.array(x) # Convert the list to a numpy array
    Y = np.array(y) 

    plt.figure(figsize=(8, 6)) # Set the figure size

    sns.set_context("paper", font_scale=1.2) 
    sns.set_style("ticks") # Set the style of the plot

    plt.scatter(X, Y, color='blue', label='Data points') # Scatter plot of the data points
    plt.plot(X, slope * X + intercept, color='red', label='Fitted line') # Plot the fitted line

    plt.xlabel(r"$\left(\frac{1}{T_2} - \frac{1}{T_1}\right) \quad [\mathrm{K}^{-1}]$") # X-axis label
    plt.ylabel(r"$\ln\left(\frac{R_1}{R_2}\right)$") # Y-axis label
    plt.title(f'Linear Regression for $\\lambda = {wl}$ nm') # Title of the plot
    plt.legend(frameon=True, edgecolor="gray") # Show legend
    #sns.despine() # Remove the top and right spines of the plot
    
    #plt.show() 
    file_path = os.path.join(folder_name, f"linear_regression_plot_{wl}.pdf")
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
        plt.plot(X, slope * X + intercept, label=f'Fitted line (λ={wl} nm)', color=color) # Plot the fitted line

    plt.xlabel(r"$\left(\frac{1}{T_2} - \frac{1}{T_1}\right) \quad [\mathrm{K}^{-1}]$") # X-axis label
    plt.ylabel(r"$\ln\left(\frac{R_1}{R_2}\right)$") # Y-axis label
    plt.title('Linear Regression for Different Wavelengths') # Title of the plot
    plt.legend(frameon=True, edgecolor="gray") # Show legend
    #sns.despine() # Remove the top and right spines of the plot
    
    #plt.show() 
    file_path = os.path.join(folder_name, f"grouped_linear_regression_plot.pdf")
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

    wave_lengths = [450, 685, 895] # Wavelengths in nm
    folder_name = 'results'
    grouped_x_data = []
    grouped_y_data = []
    slopes = []
    intercepts = []
    markers = ["o", "s", "^"]  # Different markers for each wavelength
    colors = ["blue", "green", "orange"]  # Different colors for each wavelength

    for wl in wave_lengths:
        df = read_values(f'temp_{wl}.txt')
        #print(df)
        resistance = df["Voltaje"] / df["Current"] # Ohm's Law
        #print(resistance)
        """
        T_0 : room temperature at 20°; 
        R_0 : Initial resistance = 0.5 Omhs
        alpha : Temp coeff = 4.5 * 10^-3 k^-1
        """
        temp = 293.15 + (resistance - 0.5)/ (4.5e-3)
        #print(temp)

        log_resistance = [] #Combinations of resistances
        inverse_diference_temps = [] #Combinations of temperatures

        for temp_2, resistance_2 in zip(temp, resistance): #Iterates over the temperatures and resistances
            for temp_1, resistance_1 in zip(temp, resistance): #Iterates only over the smaller ones
                if temp_2 > temp_1:
                    inverse_diference_temps.append(1/temp_2 - 1/temp_1)
                    log_resistance.append(np.log(resistance_1/resistance_2))

        #print(inverse_diference_temps)
        #print(log_resistance)

        print(f"\t--- Data for wavelength {wl} nm: ---")
        slope, intercept, r_squared = linear_regression(inverse_diference_temps, log_resistance)
        print(f"Slope: {slope}")
        print(f"Intercept: {intercept}")
        print(f"R-squared: {r_squared}")

        individual_plot(wl, inverse_diference_temps, log_resistance, slope, intercept)

        # Store the data for grouped plotting
        grouped_x_data.append(inverse_diference_temps)
        grouped_y_data.append(log_resistance)
        slopes.append(slope)
        intercepts.append(intercept)

    grouped_plot(wave_lengths, grouped_x_data, grouped_y_data, slopes, intercepts, markers, colors)


if __name__ == "__main__":
    main()