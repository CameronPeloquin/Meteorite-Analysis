"""
Contains code to plot a barplot of the counts for meteors in
low and high areas of population and vegetation.
"""
import numpy as np
import pandas as pd
import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt

# Latitude above antarctica to filter out meteor strikes from it.
# Antarctica is excluded because it contains the vast majority of
# meteors in the dataset.
FILTER_ANTARCTIC = -60

# Filter year on meteors for population, as population
# distribution was likely very different from today before 1900.
FILTER_YEAR = 1900

def plot_bar(data, popup=False):
    """
    Plots a barplot showing the number of meteors in low and high
    vegetation and population zones, excluding Antarctica. Shows the
    Figure if popup is true, saves it if false.
    """
    plt.close()
    pop_data = data['pop_tiles']
    veg_data = data['veg_tiles']
    strikes = data['strikes']

    # Filters out data from Antarctica
    strikes = strikes[ strikes['lat'] > FILTER_ANTARCTIC ]

    # Filters meteors without a year found, and those found before 1900
    strikes['year'] = strikes['year'].str.slice(start=6, stop=10)
    strikes.year.fillna(0, inplace=True)
    strikes['year'] = strikes['year'].astype(int)
    recent_strikes = strikes[ strikes['year'] > FILTER_YEAR ]
    print("Meteor Strikes post 1900: {}".format(recent_strikes['year']))

    meteors_pop = create_plot_data(pop_data, recent_strikes, 'Population')
    meteors_veg = create_plot_data(veg_data, strikes, 'Vegetation')

    fig, [ax1, ax2] = plt.subplots(2)
    fig.tight_layout()
    sns.countplot(x='Population', data=meteors_pop, ax=ax1)
    sns.countplot(x='Vegetation', data=meteors_veg, ax=ax2)
    

    if popup:
        plt.show()
    else:
        plt.savefig('plot_bar.png')

def create_plot_data(data, strikes, label):
    """
    Converts the data into a pandas dataframe containing
    the counts of meteors that have landed in locations
    marked with high and low population or vegetaion and 
    returns it.
    """

    # Splits data into high and low groups.
    median = data['val'].median()
    high = data[ data['val'] > median ]
    low = data[ data['val'] <= median ]

    # Calculates the number of meteors that landed in
    # high and low areas
    high_meteors = gpd.sjoin(high, strikes, op='intersects')
    low_meteors = gpd.sjoin(low, strikes, op='intersects')
    num_high = len(high_meteors)
    num_low = len(low_meteors)

    # Puts data into a dataframe that can be used to create a count plot
    high_count = np.full((num_high,), 'High ' + label)
    low_count = np.full((num_low,), 'Low ' + label)
    count = np.concatenate((high_count, low_count))
    meteors = pd.DataFrame()
    meteors[label] = count
    return meteors


if __name__ == '__main__':
    from ingest import ingest_all_data
    #plot_bar( ingest_all_data(fileset='test'), popup=True )
    plot_bar( ingest_all_data(), popup=True )