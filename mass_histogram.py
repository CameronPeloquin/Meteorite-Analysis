"""
Contains code to plot a histogram of
meteorites based on the Natural Log of their Mass.
"""
import numpy as np
import pandas as pd
import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt

MASS_BINS = 150


def plot_mass_hist(data, popup=False):
    """
    Plots a histogram of the Natural Log value for mass
    of the Meteorite Landings dataset. Shows the figure if
    popup = true, and saves it if popup is false
    """
    plt.close()
    strikes = data['strikes']

    # Plots histogram with ln_mass column
    strikes['ln_mass'].hist(bins=MASS_BINS)

    # Labels plot
    plt.xlabel('Mass (ln grams)')
    plt.ylabel('Count')
    plt.title('Histogram of Mass (Natural Log Scale)')
    
    if popup:
        plt.show()
    else:
        plt.savefig('mass_hist.png')


if __name__ == '__main__':
    from ingest import ingest_all_data
    #plot_mass_hist( ingest_all_data(fileset='test'), popup=True )
    plot_mass_hist( ingest_all_data(), popup=True )
