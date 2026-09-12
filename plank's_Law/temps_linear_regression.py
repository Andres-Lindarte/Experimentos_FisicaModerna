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

def plot_data(wl, x, y, slope, intercept, folder_name='results'):

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
    
    #plt.show() # Show the plot
    file_path = os.path.join(folder_name, f"linear_regression_plot_{wl}.pdf")
    plt.savefig(file_path, dpi=300, bbox_inches='tight') # Save the plot as a PDF file
    plt.close() # Close the plot to free memory

def main():
    wave_lengths = [450, 685, 895] # Wavelengths in nm
    folder_name = 'results'

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

        plot_data(wl, inverse_diference_temps, log_resistance, slope, intercept)

if __name__ == "__main__":
    main()