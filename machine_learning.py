"""
Contains code to create a regression model for predicting
the latitude of a meteor strike based on its characteristics.

Longitude is not compared due to the earths spin relative to
the plane of the solar system.

There appears to be no correlation between the two due to a very
high root mean squared value reported from the model.
"""
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


def regression_model(data):
    """
    Runs a regression model to explore if there is a relationship between 
    where a meteor was found, and its characteristics.
    """
    strikes = data['strikes']

    # Filter out unneeded columns, and dummy encodes categorical data
    #del strikes['ln_mass']
    del strikes['mass']
    del strikes['name']
    del strikes['year']
    del strikes['long']
    del strikes['geometry']
    del strikes['fall']
    strikes = pd.get_dummies(strikes)
    
    # Run the machine learning analysis comparing latitude to mass and type
    X = strikes.loc[:, strikes.columns != 'lat' ]
    y = strikes['lat']
    X_train , X_test , y_train , y_test = train_test_split(X, y, test_size=0.2)
    model = DecisionTreeRegressor()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print("Latitude regression mean squared error: {}".format(mean_squared_error(y_pred, y_test)))


if __name__ == '__main__':
    from ingest import ingest_all_data
    #regression_model(ingest_all_data(fileset='test'))
    regression_model(ingest_all_data())
