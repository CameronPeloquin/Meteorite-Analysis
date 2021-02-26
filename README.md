# Relationships Between Meteorite Landings, Vegetation, and Population Density

Background:
    This project explores if there is any correlation between where 
    meteorites are found vs. population and vegetation density.
    It also tests the correlation between meteorite characteristics
    and the latitude it falls. 
    
Installation:

    1. Create a Python Virtual Environment and activate it
        - pip install virtualenv
        - virtualenv _name_of_virtual_environment_
        - _name_of_virtual_environment_\Scripts\activate.bat
    
    2. Install requirements

    If running on Linux, Mac or in Anaconda, the following should install libraries:

        pip install -r requirements.txt

    If running Windows and that doesn't work, this sequence should 
    install needed libraries (https://stackoverflow.com/questions/54734667/error-installing-geopandas-a-gdal-api-version-must-be-specified-in-anaconda):
        - pip install wheel
        - pip install pipwin 
        - pipwin install numpy
        - pipwin install pandas
        - pipwin install shapely
        - pipwin install gdal
        - pipwin install fiona
        - pipwin install pyproj
        - pipwin install six
        - pipwin install rtree
        - pipwin install geopandas
        - pipwin install scikit-learn
        - pipwin install matplotlib
        - pipwin install seaborn

Running the project:

    To run the entire analysis:

        - python main.py
        running with default creates heat_map.png, plot_bar.png, and mass_hist.png

        - python main.py [test|default|large]
        'test', 'default', and 'large' arguments will run different granularity of data sets, 
        and display popup charts. 

    To run individual pieces of the analysis with default data:
        - python _filename_.py
    
    To get the Meteorite_Small.csv database:
        - python utils.py

Databases Used:
    Vegetation Density
        - https://neo.sci.gsfc.nasa.gov/view.php?datasetId=MOD_NDVI_M
        - CSV format
        - To use 1.0 degree version pass 'test' into fileset for ingest_all_data
        - To use 0.5 degree version pass 'default' into fileset for ingest_all_data
        - To use 0.1 degree version pass 'large' into fileset for ingest_all_data
        - Date used is August 2019
    
    Population Density
        - https://neo.sci.gsfc.nasa.gov/view.php?datasetId=SEDAC_POP
        - CSV format
        - To use 1.0 degree version pass 'test' into fileset for ingest_all_data
        - To use 0.5 degree version pass 'default' into fileset for ingest_all_data
        - To use 0.1 degree version pass 'large' into fileset for ingest_all_data
        - Date used is January 2000
    
    Meteorite Landings
        - https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh
        - CSV format
    
