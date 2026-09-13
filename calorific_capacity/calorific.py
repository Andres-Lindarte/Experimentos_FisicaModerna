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
    points = pd.read_csv(f"data/{file_name}", sep='\\s+', header=None, names=['Time', 'Mass'])
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

def plot_data(metal_name, x, y, slope_1, slope_2, intercept_1, intercept_2, folder_name='results'):

    os.makedirs(folder_name, exist_ok=True) # Create the folder if it doesn't exist

    X = np.array(x) # Convert the list to a numpy array
    Y = np.array(y) 

    plt.figure(figsize=(8, 6)) # Set the figure size

    sns.set_context("paper", font_scale=1.2) 
    sns.set_style("ticks") # Set the style of the plot

    plt.scatter(X, Y, color='blue', label='Data points') # Scatter plot of the data points
    plt.plot(X, slope_1 * X + intercept_1, color='red', label='Fitted line') # Plot the fitted line

    plt.xlabel(r"$\left(\frac{1}{T_2} - \frac{1}{T_1}\right) \quad [\mathrm{K}^{-1}]$") # X-axis label
    plt.ylabel(r"$\ln\left(\frac{R_1}{R_2}\right)$") # Y-axis label
    plt.title(f'Linear Regression for $\\lambda = {wl}$ nm') # Title of the plot
    plt.legend(frameon=True, edgecolor="gray") # Show legend
    #sns.despine() # Remove the top and right spines of the plot
    
    #plt.show() # Show the plot
    file_path = os.path.join(folder_name, f"linear_regression_plot_{wl}.pdf")
    plt.savefig(file_path, dpi=300, bbox_inches='tight') # Save the plot as a PDF file
    plt.close() # Close the plot to free memory