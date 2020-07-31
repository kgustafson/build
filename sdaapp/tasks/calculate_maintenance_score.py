import pandas as pd
from datetime import datetime
import numpy as np
import os
import sys

# Set Directory (can skip if script run in same directory as data)
directory = "/usr/local/airflow/processed_data"
os.chdir(directory)

# Set filename
try:
    filename = str(sys.argv[1])
except ValueError:
    print("invalid filename")

# Read in Data
df = pd.read_csv(filename)

### Set variables ###
fluid_density = 1025 # kg/m^3
reference_area = 1000 # m^2
drag_coefficient = 0.295
gravity = 9.81
surf_threshold = 30 # setting depth threshold for surfacing
# Other critical depth thresholds?
W_depth = .000005 # maintenance-depth per-minute equivalence weighting ---- is this non-linear?
W_depthrate = 10 # maintenance-depth rate equivalence weighting ---- is this non-linear?
W_stress = 1 # maintenance weighting related to hull stress
# W_cycles = 500 # maintenance weighting related to dive cycles
W_cycles = 250 # maintenance weighting related to dive cycles
W_depthchange = 0.005 # maintenance weighting related to depth changes
W_drag = 0.000000001 # maintenance weighting related to drag
cycle_width = 200 # minimum width of a depth cycle
num_surfaces = 0 # number of times the sub surfaces from a dive
num_dives = 0 # number of times the sub dives from the surface
weighted_depth_sum = 0 # weighted maintenance impact of time spent at different depths (on a per-minute basis)
weighted_hdot_sum = 0 # weighted maintenance impact of depth changes
num_cycles = 0 # number of dive cycles

### Functions to generate columns ###
def calculate_drag(speed):
    drag = (fluid_density * ((speed/1.944)**2) * reference_area * drag_coefficient)/2
    return drag

def calculate_pressure(depth):
    pressure = fluid_density * gravity * (depth / 3.281)
    return pressure

def number_of_dives(df): # calculate number of dives given method above
    df['surface_bool'] = (df['Depth'] <= surf_threshold).astype(int)
    num_dives = len(df[df.surface_bool.diff() < 0])
    return num_dives  

def number_of_surfaces(df): # calculate number of surfaces given method above
    df['surface_bool'] = (df['Depth'] <= surf_threshold).astype(int)
    num_surfaces = len(df[df.surface_bool.diff() > 0])
    return num_surfaces

def weighted_depth_sum_func(df):
    df['depth_weighted'] = df['Depth']*W_depth
    depth_sum = df.depth_weighted.sum()
    return depth_sum

def weighted_depth_rate_func(df): # edit ordering
    df['hdot'] = df.Depth.diff()
    df['hdot_abs'] = df['hdot'].abs()
    df = df.fillna(0)
    if df['hdot_abs'].sum()==0:
        return 0.0
    array = df['hdot_abs'].to_numpy().nonzero()
    values = df['hdot_abs'].iloc[array[0]]
    return values.sum()/values.size*W_depthrate

def weighted_depth_change(df):
    cum_weighted_depth_change = (abs(df.Depth.diff())*W_depthchange).sum()
    return cum_weighted_depth_change

def compute_cycles(df):
    num_cycles = 0
    is_upcycle = False
    is_downcycle = False
    low_val = df['Depth'].iloc[0]
    high_val = df['Depth'].iloc[0]
    for i,row in df.iterrows():
        # If in cycle, check cycle completion
        if is_upcycle:
            if row['Depth'] < high_val - cycle_width:
                # Found cycle end
                num_cycles += 1
                # Reset low/High values
                low_val = row['Depth']
                high_val = row['Depth']
                is_upcycle = False
        elif is_downcycle:
            if row['Depth'] > low_val + cycle_width:
                # Found cycle end
                num_cycles += 1
                # Reset low/High values
                low_val = row['Depth']
                high_val = row['Depth']
                is_downcycle = False
        else:
            # If not in cycle, check if a new cycle is started
            if row['Depth'] > low_val + cycle_width:
                is_upcycle = True
                high_val = row['Depth']
            if row['Depth'] < high_val - cycle_width:
                is_downcycle = True
                low_val = row['Depth']
        # Update low/high values
        if row['Depth'] < low_val:
            low_val = row['Depth']
        elif row['Depth'] > high_val:
            high_val = row['Depth']
    return num_cycles

def compute_cycles_surf(df):
    surfaces = number_of_surfaces(df)
    dives = number_of_dives(df)
    return min(surfaces,dives)

def add_columns_to_df(df):
    df['Drag'] = df['Speed'].apply(calculate_drag)
    df['Pressure'] = df['Depth'].apply(calculate_pressure)
    df['Weighted_Drag'] = df.Drag*W_drag
    df['Weighted_Pressure'] = df.Pressure*0.00005
    df['Change_in_Pressure'] = abs(df['Pressure'].diff())
    df['surface_bool'] = (df['Depth'] <= surf_threshold).astype(int)
    df['weighted_depth'] = df['Depth']*W_depth
    df['hdot'] = df.Depth.diff()
    df['hdot_abs'] = df.hdot.abs()
    df['depth_change'] = df.Depth.diff()
    df['depth_change_abs'] = df['depth_change'].abs()
    df['weighted_depth_change'] = df['depth_change_abs']*W_depthchange
    df['Speed_diff'] = df.Speed.diff()
    df['Speed_diff_abs'] = abs(df.Speed.diff())
    df = df.fillna(0)
    return df

def scenario_results(df):
    start_time = df['Time'].iloc[0]
    stop_time = df['Time'].iloc[-1]
    weighted_depth_sum = df['weighted_depth'].sum()
    weighted_drag_sum = df['Weighted_Drag'].sum()
    weighted_hdot_sum = weighted_depth_rate_func(df)
    weighted_depth_change_sum = df['weighted_depth_change'].sum()
    total_weighted_stress = W_stress*(weighted_depth_sum + weighted_hdot_sum + weighted_depth_change_sum + weighted_drag_sum)
    weighted_cycles = compute_cycles_surf(df)*W_cycles
    maintenance_score = weighted_cycles + total_weighted_stress
    matrix = pd.DataFrame([[start_time, stop_time, maintenance_score, weighted_cycles, total_weighted_stress, weighted_depth_sum, 
                            weighted_depth_change_sum, weighted_hdot_sum, weighted_drag_sum]], 
                            columns=['Start Time', 'Stop Time', 'Maintenance Score', 'Weighted Cycles', 'Total Stress', 
                                     'Weighted Depth', 'Weighted Depth Change', 'Weighted Depth Rate', 'Weighted Drag'])
    return matrix
#    return maintenance_score

# Calculate maintenance score
df = add_columns_to_df(df)

# Change directory
directory = "/usr/local/airflow/results"
os.chdir(directory)

# Append updated results
try:
    results_df = pd.read_csv("results.csv")
    results_df = results_df.append(scenario_results(df))
except:
    results_df = scenario_results(df)

# Write to .csv file in same directory
results_df.to_csv("results.csv", index=None)

print('Updated Results File')


