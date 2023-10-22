import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from map_utils import *


# Load the CSV data into a DataFrame
channel_map_df = pd.read_csv('channel_map.csv')

# Replace NaN values in 'SG ch#' with a placeholder and convert the rest to integers
channel_map_df['SG ch#'] = channel_map_df['SG ch#'].\
    where(channel_map_df['SG ch#'].notna(), 'NaN').astype(
        str).str.split('.').str[0]


# Scatter plot
fig, ax = plt.subplots(figsize=(10, 10))
ax.scatter(channel_map_df['X, um'], channel_map_df['Y, um'],
           color='black', s=50)  # black filled circles

# Add text label to the left of each point
for i, txt in enumerate(channel_map_df['Pad #']):
    ax.annotate(txt, (channel_map_df['X, um'].iloc[i], channel_map_df['Y, um'].iloc[i]),
                fontsize=6, ha='right', va='center', xytext=(-5, 0), textcoords='offset points')

for i, txt in enumerate(channel_map_df['SG ch#']):
    ax.annotate(txt, (channel_map_df['X, um'].iloc[i], channel_map_df['Y, um'].iloc[i]),
                fontsize=6, ha='right', va='center', xytext=(17, 0), textcoords='offset points')

# Set title and labels

ax.set_xlabel('X, um')
ax.set_ylabel('Y, um')
plt.tight_layout()
plt.xlim([-100, 100])
plt.show()


# %% Create dictionaries that map one set of IDs to another set of IDs

# Load the CSV data into a DataFrame
channel_map_df = pd.read_csv('channel_map.csv')
electrode_IDs = channel_map_df['Pad #']
electrode_pos = channel_map_df[['X, um', 'Y, um']]


# Testing the functions
left_flex_IDs, right_flex_IDs, left_flex_pos, right_flex_pos = create_flex_cable_ids()


SG_IDs = channel_map_df['SG ch#']


electrode_to_flex = channel_map_df.set_index('Pad #')['SG ch#'].to_dict()
