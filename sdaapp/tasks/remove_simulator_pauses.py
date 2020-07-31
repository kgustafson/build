##### Remove data rows when simulator is not running but data is being generated #####
# Import Libraries 
import pandas as pd
from datetime import datetime
import numpy as np
import os

# Set Directory (can skip if script run in same directory as data)
directory = "/usr/local/airflow/data"
os.chdir(directory)

# Set filename
filename = "Day2_subset_with_outliers_tagged.csv"

# Read in Data
df = pd.read_csv(filename)

### Label columns that are identical to the previous column in Course, Speed,
### Speed Over Ground, Depth Rate, and Depth metrics ###
df['match'] = (df['Course'].eq(df['Course'].shift()) & 
               df['Speed'].eq(df['Speed'].shift()) & 
               df['Speed_Over_Ground'].eq(df['Speed_Over_Ground'].shift()) & 
               df['Depth_Rate'].eq(df['Depth_Rate'].shift()) & 
               df['Depth'].eq(df['Depth'].shift()))

### Create column to count number of consecutive identical rows ###
# Generate increment list indicating number of consecutive identical rows
ct = 0 # begin count increment
count_list = [] # create empty list to be appended to
for i in range(df.shape[0]): # iterate through each row
    if df.match.iloc[i].any(): # if 'match' column equal to 'True'
        ct += 1 # increment
    else:
        ct = 0 # reset increment
    count_list.append(ct) # append increment to list
    
# Add increment count list to a column in the dataframe
df['match_count'] = count_list

### Set threshold for consecutive seconds with no changes in data ###
seconds_threshold = 6000 # 6000 seconds, or 100 minutes

### Remove all rows of data where the threshold is exceeded ###
df_pauses_removed = df[df.match_count < seconds_threshold].reset_index()

# Drop 'index', 'match', and 'match_count' columns
df_pauses_removed = df_pauses_removed.drop(columns=['match','match_count','index'])

### Write wrangled dataframe to a .csv file ###
# Set filename
written_filename = "{}_wrangled_df.csv".format(filename.split('_')[0])

# Write to .csv file in same directory
df_pauses_removed.to_csv(written_filename, index=None)

# Print statement indicating the dataframe was written to a .csv format
print(written_filename + ' written to .csv file.')
