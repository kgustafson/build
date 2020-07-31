### Subset Dataframe and write it to new .csv file ###
# Import Libraries
import pandas as pd
import os
import sys

# Set Directory (can skip if script run in same directory as data)
directory = "/usr/local/airflow/ingest"
os.chdir(directory)

# Set filename
try:
    filename = str(sys.argv[1])
except ValueError:
    print("invalid filename")

# Read in Data
df = pd.read_csv(filename)

### Subset Dataframe ###
# Define subset function
def subset_data(df):
    # Interested in 7 columns (Course, Speed Through Water, Speed Over Ground,
    #                          Depth Rate, Depth, Heading, and Time)
    # Identify column names to subset
    columns_of_interest = ["Info.Motion.GeoVelocity.Course.Value", 
                           "Info.Motion.SpeedThroughWater.Value",
                           "Info.Motion.SpeedOverGround.Value", 
                           "Info.Position.Depth.DepthRate.Value",
                           "Info.Position.Depth.KeelDepthUnderSail.Value", 
                           "Info.Attitude.CommonAttitude.GeoHeading.Value", 
                           "MasterTime"]
    
    # Subset on "columns_of_interest"
    df = df[columns_of_interest]
    
    # Set shorter column names
    df.columns = 'Course Speed Speed_Over_Ground Depth_Rate Depth Heading Time'.split()
    
    # Return subset dataframe
    return df

# Subset dataframe
subset_df = subset_data(df)

### Write subset_data to a .csv file ###
# Change directory
directory = "/usr/local/airflow/processed_data"
os.chdir(directory)
# Set filename
base_filename = os.path.basename(filename)
written_filename = "{}_subset.csv".format(base_filename.split('.')[0])

# Write to .csv file in same directory
subset_df.to_csv(written_filename, index=None)

# Print statement indicating the dataframe was written to a .csv format
print(written_filename + ' written to .csv file.')
