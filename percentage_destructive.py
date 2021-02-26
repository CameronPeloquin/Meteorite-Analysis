"""
Contains code to calculate the rate per square kilometer per year
of destructive meteor strikes.
"""
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon

# Arbitrary mass for a meteor to be considered destructive in grams
DESTRUCTIVE_METEOR_MASS = 1808

# Latitude and Longitude coordinates that are used to generate a polygon
# that represents an area of Antarctica with high meteor density.
# This area is used because there is a large operation for discovering
# meteors there. Assuming the density of meteor falls per area is the same around the globe,
# this area represents the density of the meteors that fall everywhere.
POLYGON_LEFT = 151
POLYGON_RIGHT = 170
POLYGON_TOP = -70
POLYGON_BOTTOM = -82

# Area of polygon that was measured using Google Earth in square kilometers
AREA_ANTARCTIC = 700000

# Estimate of the timespan when the meteors found in Antarctica fell
YEARS_DATA_REPRESENTS = 100000


def calculate_percent_destructive(data):
    """
    calculate the rate per square kilometer per year
    of destructive meteor strikes. By using Antarctica as
    a the baseline.
    """
    strikes = data['strikes']

    # Filter strikes in area of Antarctica
    antarctic = Polygon([(POLYGON_LEFT, POLYGON_TOP), (POLYGON_RIGHT, POLYGON_TOP),
        (POLYGON_RIGHT, POLYGON_BOTTOM), (POLYGON_LEFT, POLYGON_BOTTOM)])
    strikes = strikes[ strikes['geometry'].within(antarctic) == True ]

    # Calculate percentage of destructive meteors.
    destructive_strikes = strikes[ strikes['mass'] > DESTRUCTIVE_METEOR_MASS ]
    num_destructive = len(destructive_strikes)
    print("Number of destructive meteors: {}".format(num_destructive))
    print("Number of total meteors: {}".format(len(strikes)))
    percent_destructive = (num_destructive / len(strikes)) * 100
    print("Percentage of destructive meteors: {}".format(percent_destructive))
    
    print("Area of Antarctic region: {}".format(AREA_ANTARCTIC))
    destructive_density = num_destructive / AREA_ANTARCTIC
    print("Density of destructive meteor falls: {}".format(destructive_density))
    destructive_rate = destructive_density / YEARS_DATA_REPRESENTS
    print("Destructive rate per square km per year: {}".format(destructive_rate))


if __name__ == '__main__':
    from ingest import ingest_all_data
    #calculate_percent_destructive(ingest_all_data(fileset='test'))
    calculate_percent_destructive(ingest_all_data())
