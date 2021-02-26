"""
Contains code to plot a heat map of vegetation and population density.
As well as a scatterplot of all meteorstrikes in the dataset.
"""
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

WORLD_COLOR = '#EEEEEE'

# Empty data value for population dataset
EMPTY_POP_VALUE = 1.04

# Lowest vegetation density value is -0.1, so 0 is used to
# represent low vegetation
LOW_VEG_VALUE = 0

# Marker size for meteors is based on mass of meteor.
# For a better visualization the ln of the mass is used,
# and it is scaled down by this factor.
METEOR_MARKER_TUNING = 0.03

def plot_heat_maps(data, popup=False):
    """
    Plots a figure containing a heat map of population
    and vegetation density, as well as a scatter plot showing
    all meteorstrikes in the dataset. Shows figure if popup is true.
    Saves it if popup is false.
    """
    plt.close()
    pop_data = data['pop_tiles']
    veg_data = data['veg_tiles']
    strikes = data['strikes']

    # For better display remove empty pop and low veg, scale pop, strikes
    pop_data = pop_data[ pop_data['val'] != EMPTY_POP_VALUE ]
    veg_data = veg_data[ veg_data['val'] > LOW_VEG_VALUE ]
    pop_data['lg_val'] = np.log10(pop_data['val'])
    strikes['size'] = strikes['ln_mass'] * METEOR_MARKER_TUNING

    # Plots the figure
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    fig, [ax1, ax2, ax3] = plt.subplots(3)
    fig.tight_layout()
    world.plot(ax=ax1, color=WORLD_COLOR, edgecolor=None)
    world.plot(ax=ax2, color=WORLD_COLOR, edgecolor=None)
    world.plot(ax=ax3, color=WORLD_COLOR, edgecolor=None)
    pop_data.plot(column='lg_val', ax=ax1, edgecolor=None, legend=True)
    veg_data.plot(column='val', ax=ax2, edgecolor=None, legend=True)
    strikes.plot(ax=ax3, marker='.', color='red', markersize=strikes['size'], alpha=0.1)
    ax1.set_title('Heat Map of Population Density (Log10 Scale)')
    ax2.set_title('Heat Map of Vegetation Density')
    ax3.set_title('Meteor Strikes')

    if popup:
        plt.show()
    else:
        plt.savefig('heat_map.png')


if __name__ == '__main__':
    from ingest import ingest_all_data
    #plot_heat_maps( ingest_all_data(fileset='test'), popup=True )
    plot_heat_maps( ingest_all_data(), popup=True )
