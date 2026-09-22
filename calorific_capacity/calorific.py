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

def calorific_capacity(mass_metal, intercepts):
    L = 47.6   # Constant of the nitrogen [cal/g]
    delta_temp = 216.5  # Since Ni is at 77K
    delta_mass = intercepts[0] - intercepts[2]
    cal_capacity = (L * delta_mass) / (mass_metal * delta_temp)
    return delta_mass, cal_capacity

def relative_error(measured, true):
    error = abs(measured - true) / true * 100
    return error

def grouped_plot(figure_number, metal, x_data, y_data, slopes, intercepts, last_time, folder_name='results'):

    os.makedirs(folder_name, exist_ok=True) # Create the folder if it doesn't exist

    plt.figure(figsize=(8, 6)) # Set the figure size

    sns.set_context("paper", font_scale=1.2) 
    sns.set_style("ticks") # Set the style of the plot

    for x, y, slope, intercept in zip(x_data, y_data, slopes, intercepts):
        X = np.array(x) # Convert the list to a numpy array
        Y = np.array(y) 
        plt.scatter(X, Y) # Scatter plot of the data points
        if slope is not None and intercept is not None:
            X_full_range = np.linspace(0, last_time, 100) # Create a range of x values for the fitted line
            plt.plot(X_full_range, slope * X_full_range + intercept) # Plot the fitted line

    plt.xlabel("Time (s)") # X-axis label
    plt.ylabel("Mass (g)") # Y-axis label
    plt.title(f'Figure {figure_number + 1}: Mass as function of time for {metal.capitalize()}') # Title of the plot
    #plt.legend(frameon=True, edgecolor="gray") # Show legend
    #sns.despine() # Remove the top and right spines of the plot
    
    #plt.show() 
    file_path = os.path.join(folder_name, f"{metal}_mass_change.pdf")
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

    metals = ['lead', 'aluminum', 'copper', 'zinc', 'tin']
    metals_mass = [229.0, 9.7, 192.5, 62.2, 57.9] # Experimental data
    real_calorific_capacity = [0.031, 0.214, 0.092, 0.093, 0.054] # Real calorific capacity values [cal/g·K]

    fout = open("results/results.txt", "w") # Open a file to write the results
    fout.write("\t--- Calorific Capacity Results: ---\n")
    for number, solid in enumerate(metals): # Get the metals data
        time_data = []
        mass_data = []
        slopes = []
        intercepts = []
        for ii in range(1, 4): # Get the three phases of the montage 
            # Read the data
            file_name = f"{solid}_{ii}.txt"
            points = read_values(file_name)
            time = points['Time']
            mass = points['Mass']
            # Calculate the lines for phase 1 and 3
            if ii == 1 or ii == 3:
                slope, intercept, _ = linear_regression(time, mass)
                slopes.append(slope)
                intercepts.append(intercept)
            else: 
                slopes.append(None)
                intercepts.append(None)
            # Groups the x and y data for the grouped plot
            time_data.append(time)
            mass_data.append(mass)
        delta_mass, cal_capacity = calorific_capacity(mass_metal=metals_mass[number], intercepts=intercepts) 
        porcentual_rel_error = relative_error(cal_capacity, real_calorific_capacity[number])
        fout.write(f"Metal: {solid.capitalize()}, Δm: {delta_mass:.4f} g, Calorific Capacity: {cal_capacity:.4f} cal/g·K, Relative Error: {porcentual_rel_error:.2f}%\n")
        fout.close() # Close the file after writing all results

        grouped_plot(number, solid, time_data, mass_data, slopes, intercepts, last_time=max([max(t) for t in time_data]), folder_name='results')

if __name__ == "__main__":
    main()