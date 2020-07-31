##### Tag outliers in data and impute values #####
# Import Libraries 
import pandas as pd
from datetime import datetime
import numpy as np
import os

# Set Directory (can skip if script run in same directory as data)
directory = "/usr/local/airflow/data"
os.chdir(directory)

# Set filename
filename = "Day2_subset.csv"

# Read in Data
df = pd.read_csv(filename)

### Find outliers ###
# Define function to identify and tag outliers in an "Outliers" column
def find_outliers(df):
    # Mark outliers
    df['Outlier'] = np.where(((abs(df['Depth_Rate'] - df['Depth_Rate'].shift(1))) > 250) | # Depth Rate
                             ((abs(df['Speed'] - df['Speed'].shift(1))) > 15) | # Speed
                             ((abs(df['Speed_Over_Ground'] - df['Speed_Over_Ground'].shift(1))) > 15), # Speed Over Ground
                             "True", "False")
    # Return dataframe
    return df

# Create outlier dataframe
outlier_df = find_outliers(df)

# Create a list of indices where Outlier == 'True'
outlier_index_list = outlier_df[outlier_df.Outlier == 'True'].index.tolist()

# Generate list of columns where we want to impute the values
col_list = outlier_df.columns.difference(['Time','Outlier']).tolist()

### Impute values of outlier rows ###
# Loop through each row and column to impute values
for row_num in outlier_index_list:
    for col in col_list:
        outlier_df.loc[row_num, col] = outlier_df.loc[row_num - 1, col]

### Write data tagged of outliers and outliers imputed to a .csv file ###
# Set filename
written_filename = "{}_with_outliers_tagged.csv".format(filename.split('.')[0])

# Write to .csv file in same directory
outlier_df.to_csv(written_filename, index=None)

# Print statement indicating the dataframe was written to a .csv format
print(written_filename + ' written to .csv file.')
