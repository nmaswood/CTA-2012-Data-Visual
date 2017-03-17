import pandas as pd
import numpy as np

def _common_replacements(input_str):

    replacements = (
        ("Street", "St"),
        ("Avenue", "Ave"),
        ("Road", "Rd"),
        ("Boulevard", "Blvd"),
        ("Drive", "Dr")
    )

    for (to_replace, to_replace_with) in replacements:

        input_str = input_str.replace(to_replace, to_replace_with)

    return input_str

def read_data():

    data = pd.read_csv("traffic.csv")
    data_prime = data.copy()
    cols = data_prime.columns
    cols_to_remove = [cols[0], cols[1], cols[3], cols[5], cols[8]]

    data_dropped = data_prime.drop(cols_to_remove, axis =1)

    data_dropped['Street'] = data_dropped['Street'].apply(_common_replacements)
    data_prime_prime = data_dropped.sort_values(
        by = ['Total Passing Vehicle Volume'],
        ascending = False).reset_index()

    data_prime_prime_prime = data_prime_prime.drop([data_prime_prime.columns[0]], axis = 1)

    return data_prime_prime_prime
