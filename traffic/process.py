import pandas as pd
import numpy as np

def read_data():

    data = pd.read_csv("traffic.csv")
    data_prime = data.copy()
    cols = data_prime.columns
    cols_to_remove = [cols[0], cols[1], cols[3], cols[5], cols[6], cols[7]]

    return data_prime.drop(cols_to_remove, axis =1)

def write_data():

    data = read_data()
    data.to_csv("traffic_prime.csv")

