import numpy as np
import pandas as pd

# Read the file 
def read_values(file_name):
    points = pd.read_csv(file_name, sep='\s+', header=None, names=['Voltaje', 'Current', 'Value'])
    return points 

def main():
    data = read_values('temps_450.txt')
    print(data)


