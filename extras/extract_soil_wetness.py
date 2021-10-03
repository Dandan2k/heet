# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A script that extracts the soil wetness of a dam from a .txt database.

Notes:
    * This code can be greatly improved, since the latitudes and longitudes are
    already sorted. This means that there's no need to actually load the entire
    database. You can do a preliminary search over latitude and longitude to
    find the pixel you need. However, I need to look into how to actually
    implement this.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Created: 19/08/2021
Last Updated: 19/08/2021

Author: Daniel-Alexandru Nistor
"""
import pandas as pd

def compute_soil_wetness(latitude, longitude):
    '''
    A function that computes the mean soil wetness over the year for a given
    latitude-longitude position.
    '''
    # A list of column names.
    col_names = ['Longitude', 'Latitude', 'Wetness Jan', 'Wetness Feb',
                 'Wetness Mar', 'Wetness Apr', 'Wetness May', 'Wetness Jun',
                 'Wetness Jul', 'Wetness Aug', 'Wetness Sep', 'Wetness Oct',
                 'Wetness Nov', 'Wetness Dec']
    # The step size (precision) when it comes to longitude and latitude in the
    # database. This can be deducted, not hardcoded, but there's not much
    # reason to this for now.
    step = 0.5
    # Note that the data is weirdly separated (not just single-spaced).
    data = pd.read_csv('soil_wetness_data.txt', delim_whitespace=True,
                       header=None, names=col_names)
    
    # Find the correct index in the data given the latitude and longitude of
    # the dam.
    pixel = data.loc[(longitude - step/2 < data['Longitude']) & 
                   (data['Longitude'] <= longitude + step/2) &
                   (latitude - step/2 < data['Latitude']) &
                   (data['Latitude'] <= latitude + step/2)]
    
    # Compute the mean soil wetness for the selected dam.
    mean_wetness = pixel.iloc[0, 2:].mean(axis=0)
    
    return mean_wetness

# An example testing the Kabaung dam.
print(compute_soil_wetness(18.89, 96.22))
