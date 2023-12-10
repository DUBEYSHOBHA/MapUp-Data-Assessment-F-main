import pandas as pd
import numpy as np
df = pd.read_csv('datasets/dataset-1.csv')

#q1
def generate_car_matrix(df)->pd.DataFrame:



    pivot_df = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)

    np.fill_diagonal(pivot_df.values, 0)

    return pivot_df


result_df = generate_car_matrix(df)
print(result_df)



#q2

def get_type_count(df)->dict:
   # Add a new categorical column 'car_type' based on values of the 'car' column
    conditions = [
        (df['car'] <= 15),
        (df['car'] > 15) & (df['car'] <= 25),
        (df['car'] > 25)
    ]
    choices = ['low', 'medium', 'high']
    df['car_type'] = pd.Series(np.select(conditions, choices, default=np.nan), dtype="category")

    # Calculate the count of occurrences for each 'car_type' category
    type_counts = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    type_counts = dict(sorted(type_counts.items()))
    
    return type_counts

result = get_type_count(df)
print(result)







def get_bus_indexes(df)->list:
    bus_mean = df['bus'].mean()
    
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()
    bus_indexes.sort()
    return bus_indexes

result = get_bus_indexes(df)
print(result)


def filter_routes(df)->list:
    avg_truck_per_route = df.groupby('route')['truck'].mean()
   
   
    selected_routes = avg_truck_per_route[avg_truck_per_route > 7].index.tolist()
    
    selected_routes.sort()

    return selected_routes

   


result = filter_routes(df)
print(result)



def multiply_matrix(input_df)->pd.DataFrame:
   # Create a copy of the input DataFrame to avoid modifying the original
    modified_df = input_df.copy()
    
    # Apply logic to modify values based on the given conditions
    modified_df = modified_df.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    
    # Round values to 1 decimal place
    modified_df = modified_df.round(1)
    
    return modified_df

matrix = generate_car_matrix(df)

resulting_df = pd.DataFrame(matrix)  # Replace ... with your DataFrame

modified_result = multiply_matrix(resulting_df)
print(modified_result)


def time_check(dataframe)->pd.Series:
    
    
    dataframe['start_datetime'] = pd.to_datetime(dataframe['startDay'] + ' ' + dataframe['startTime'],
                                                format='%Y-%m-%d %H:%M:%S', errors='coerce')
    dataframe['end_datetime'] = pd.to_datetime(dataframe['endDay'] + ' ' + dataframe['endTime'],
                                              format='%Y-%m-%d %H:%M:%S', errors='coerce')

    # Remove rows with missing datetime information
    dataframe = dataframe.dropna(subset=['start_datetime', 'end_datetime'])

    # Calculate the duration for each row
    dataframe['duration'] = dataframe['end_datetime'] - dataframe['start_datetime']

    # Group by unique (id, id_2) pairs
    grouped = dataframe.groupby(['id', 'id_2'])

    # Check if each group covers a full 24-hour period and spans all 7 days of the week
    completeness_check = grouped.apply(lambda x: (x['duration'].max() >= pd.Timedelta(days=1)) and
                                                (x['start_datetime'].dt.dayofweek.nunique() == 7))

    return completeness_check



# Example usage
dataset_path = 'datasets/dataset-2.csv'
df = pd.read_csv(dataset_path)
result = time_check(df)
print(result)
