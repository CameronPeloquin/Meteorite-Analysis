"""
    Utility functions
"""
import numpy as np
import pandas as pd


def data_info():
    """
    Get some info on meteorite data
    """
    mdata = pd.read_csv('Meteorite_Landings.csv')
    print(mdata.info)
    unknown = mdata[ (mdata.reclat == 0.0) & (mdata.reclong == 0.0) ]
    print("{} rows without lat/long".format(len(unknown.index)))
    #print(unknown_strikes.sample(5).to_string())
    valid = mdata[ mdata.nametype != 'Valid' ]
    print("\n{} rows without valid nametype".format(len(valid.index)))


def small_meteorite():
    """
    Make small text version of meteorite file
    """
    data = pd.read_csv('Meteorite_Landings.csv')
    print(data.info)
    drops = np.random.choice(data.index, 40000, replace=False)
    small = data.drop(drops)
    print(small.info)
    small.to_csv('Meteorite_Small.csv', index=False)


if __name__ == '__main__':
    #data_info()
    small_meteorite()
