"""
Contains code to ingest the data into a dictionary of Dataframes.
"""
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon

DATA_FOLDER = 'data/'

FILES = {
    'test': {
        'meteor': 'Meteorite_Small.csv',
        #'meteor': 'Meteorite_Landings.csv',
        'pop': 'SEDAC_POP_2000-01-01_rgb_360x180.csv',
        'veg': 'MOD_NDVI_M_2020-02-01_rgb_360x180.csv',
        },
    'default': {
        'meteor': 'Meteorite_Landings.csv',
        'pop': 'SEDAC_POP_2000-01-01_rgb_720x360.CSV',
        'veg': 'MOD_NDVI_M_2019-08-01_rgb_720x360.CSV',
        },
    'large': {
        'meteor': 'Meteorite_Landings.csv',
        'pop': 'SEDAC_POP_2000-01-01_rgb_3600x1800.CSV',
        'veg': 'MOD_NDVI_M_2020-02-01_rgb_3600x1800.CSV',
        }
    }


def ingest_all_data(fileset='default'):
    """
    Ingests the population and vegetation data 
    """
    files = FILES[fileset]
    strikes = ingest_landings(files['meteor'])
    pop_data, pop_tiles = ingest_neo(files['pop'])
    veg_data, veg_tiles = ingest_neo(files['veg'])
    print("Data ingested:", fileset)
    #print(strikes.info)
    #print(pop_data.info)
    #print(veg_data.info)
    return {
        'strikes': strikes,
        'pop_data': pop_data,
        'pop_tiles': pop_tiles,
        'veg_data': veg_data,
        'veg_tiles': veg_tiles,
        }


def ingest_neo(filename):
    """
    Load a file from neo (Near Earth Orbit) site and return a geoframe of the values,
    converting file's implied lat/long into tiles.
    Works for data sets downloaded as csv files from:
        https://neo.sci.gsfc.nasa.gov/dataset_index.php#life
        Pop CSV: https://neo.sci.gsfc.nasa.gov/servlet/RenderData?si=875430&cs=gs&format=CSV&width=720&height=360
        Veg CSV: https://neo.sci.gsfc.nasa.gov/servlet/RenderData?si=1780053&cs=rgb&format=CSV&width=720&height=360
    """
    data = pd.read_csv(DATA_FOLDER + filename, header=None, index_col=None)
    print("Read neo data: {}".format(filename))
    rows, cols = data.shape
    tile_size = 360.0 / cols
    print("Tile size: {}".format(tile_size))
    #print(data.info)

    # Loop through the columns and rows, building tile boxes
    tiles = []
    lat = 90.0
    for index, row in data.iterrows():
        lng = -180.0
        for val in row:
            # Don't add water
            if val != 99999:
                # Add tile to new data frame
                right = lng + tile_size
                bottom = lat - tile_size
                tiles.append({ 
                    'val': val, 
                    'lat': lat, 'lng': lng,
                    'tile': Polygon([ (lng, lat), (right, lat), 
                                (right, bottom), (lng, bottom) ])
                    })
            lng += tile_size
        lat -= tile_size
    tiles = gpd.GeoDataFrame(tiles, geometry='tile')
    #print(tiles)
    return data, tiles


def ingest_landings(filename):
    """
    Cleans and filters unneeded data for the meteorite landings dataset.
        https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh
        CSV: https://data.nasa.gov/api/views/gh4g-9sfh/rows.csv?accessType=DOWNLOAD&bom=true&format=true
    """
    strikes = pd.read_csv(DATA_FOLDER + filename) 

    # Remove rows not marked valid and missing or 0 lat/long 
    strikes = strikes[ strikes.nametype == 'Valid' ]
    strikes.reclat.replace(r'^\s*$', np.nan, regex=True)
    strikes.reclong.replace(r'^\s*$', np.nan, regex=True)
    strikes.reclat.fillna(0.0, inplace=True)
    strikes.reclong.fillna(0.0, inplace=True)
    strikes = strikes[ (strikes.reclat != 0.0) & (strikes.reclong != 0.0) ]

    # Clean up column names, remove ones won't use
    strikes.rename(columns={ 'mass (g)': 'mass', 'reclong': 'long', 'reclat': 'lat',
                'recclass': 'class'}, inplace=True)
    del strikes['id']
    del strikes['nametype']
    del strikes['GeoLocation']

    # Cleanup empty/zero mass, and add log size with a min size bin
    strikes.mass.fillna(0.0, inplace=True)
    strikes.mass.replace(0.0, 0.1, inplace=True)
    strikes['ln_mass'] = np.log(strikes.mass) 

    return gpd.GeoDataFrame( strikes, 
                geometry=gpd.points_from_xy(strikes['long'], strikes['lat']))

    
if __name__ == '__main__':
    #ingest_all_data()
    ingest_all_data(fileset='test')
