import numpy as np
import pandas as pd

# Read the file 
def read_values(file_name):
    """
    sep: Means the separation between values, in this case, the space 
    header: Since we don´t have headers on the raw text file
    names: Manually written headers 
    """
    points = pd.read_csv(file_name, sep='\\s+', header=None, names=['Voltaje', 'Current', 'Value'])
    return points 

def main():
    df = read_values('temp_450.txt')
    #print(df)
    resistance = df["Voltaje"] / df["Current"] # Ohm's Law
    #print(resistance)
    """
    T_0 : room temperature at 20°; 
    R_0 : Initial resistance = 0.5 Omhs
    alpha : Temp coeff = 4.5 * 10^-3 k^-1
    """
    temp = 293,15 + (resistance - 0.5)/ (4.5e-3)
    #print(temp)


if __name__ == "__main__":
    main()