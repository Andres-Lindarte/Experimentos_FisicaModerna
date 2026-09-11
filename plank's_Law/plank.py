"""
Given a temperature, we measure a "black body" spectrum, on t_1.txt
T_1: 
    V = 7.07
    I = 3.15

"""

import numpy as np
import matplotlib.pyplot as plt

def get_data(file_name):
    # Reads data from a text file and returns it as a numpy array
    return np.loadtxt(file_name)

def plot_data(wave_length, points):
    plt.figure(figsize=(10, 6))
    plt.plot(wave_length, points, marker='o', linestyle='-', color='b')
    plt.title('Data Points')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Intensity')
    plt.grid(True)
    plt.show()

def main():
    file_name = 't_1.txt'
    
    # 161 point s from 200 to 1000 nm with a step of 5 nm
    wave_length = np.arange(200, 1005 , 5)
    
    points = get_data(file_name)

    # Validate the length of wave_length and points
    if len(wave_length) != len(points):
        print(f"Attention: X has {len(wave_length)} values but the file has {len(points)} rows.")
        return

    plot_data(wave_length, points)

if __name__ == "__main__":
    main()