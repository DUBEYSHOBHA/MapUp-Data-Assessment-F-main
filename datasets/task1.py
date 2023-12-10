import pandas as pd
import numpy as np

def generate_car_matrix():

    df = pd.read_csv('datasets/dataset-1.csv')


    pivot_df = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)

    np.fill_diagonal(pivot_df.values, 0)

    return pivot_df


result_df = generate_car_matrix()
print(result_df)



