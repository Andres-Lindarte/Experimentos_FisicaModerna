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
    points = pd.read_csv(f"data/{file_name}", sep='\\s+')
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

def mean_2_values(low, high):
    return (low + high)/2

def calculate_sen_theta(diameter, long=135):
    return np.sin(2*np.arctan(diameter/(2*long))) # Calculate the sen of angle theta in radians

def calculate_inverse_squared_eV(voltaje):
    return (1/np.sqrt(voltaje*1000))

def calculate_distance_from_slope(slope):
    h = 4.1356*(10**(-15))
    m_e = 0 #TO-DO

def grouped_plot(figure_number, x_data, y_data, slope, intercept, initial_x, last_x, folder_name='results'):

    os.makedirs(folder_name, exist_ok=True) # Create the folder if it doesn't exist

    plt.figure(figsize=(8, 6)) # Set the figure size

    sns.set_context("paper", font_scale=1.2) 
    sns.set_style("ticks") # Set the style of the plot

    for x, y in zip(x_data, y_data):
        X = np.array(x) # Convert the list to a numpy array
        Y = np.array(y) 
        plt.scatter(X, Y) # Scatter plot of the data points
        X_full_range = np.linspace(initial_x, last_x, 100) # Create a range of x values for the fitted line
        plt.plot(X_full_range, slope * X_full_range + intercept) # Plot the fitted line

    plt.xlabel("1/(eV)^(1/2) [au]") # X-axis label
    plt.ylabel("sen(theta) [au]") # Y-axis label
    plt.title(f'Figure {figure_number + 1}: title') # Title of the plot
    #plt.legend(frameon=True, edgecolor="gray") # Show legend
    #sns.despine() # Remove the top and right spines of the plot
    
    #plt.show() 
    file_path = os.path.join(folder_name, f"D{figure_number}_results.pdf")
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


    fout = open("results/results.txt", "w") # Open a file to write the results
    fout.write("\t--- Calorific Capacity Results: ---\n")
    for ii in range(1, 3):
        x_data = []
        y_data = []
        file_name = f"d_{ii}.txt"
        points = read_values(file_name)

        X_data = calculate_inverse_squared_eV(points['Voltaje'])

        diameter_mean = mean_2_values(points['internal'], points['external'])
        Y_data = calculate_sen_theta(diameter_mean)

        slope, intercept, _ = linear_regression(X_data, Y_data)
        grouped_plot(ii, X_data, Y_data, slope, intercept, min(X_data), max(X_data), folder_name='results')


if __name__ == "__main__":
    main()
