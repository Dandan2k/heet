# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A program that uses the regression model we have developed in order to make
reservoir area predictions for the Myanmar dams.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Created: 17/08/2021
Last Updated: 17/08/2021

Author: Daniel-Alexandru Nistor
"""
import pandas as pd
import numpy as np
import srtm
elevation_data = srtm.get_data()

def prepare_examples():
    '''
    A function that takes the Myanmar examples and prepares them for further
    analysis by computing the dam elevation for them. The function returns the
    examples with a completed 'Elevation' column.
    '''
    # The path to the Myanmar examples. This shouldn't be hardcoded.
    examples_path = r"C:\Users\Desktop\Downloads\myanmar_regression_data.txt"
    examples = pd.read_csv(examples_path, sep='\t', header=0)

    latitudes, longitudes = examples['Latitude'], examples['Longitude']
    elevations = []

    for latitude, longitude in zip(latitudes, longitudes):
        elevations.append(elevation_data.get_elevation(latitude, longitude))
    
    examples['Elevation'] = elevations

    return examples


def compute_predictions():
    '''
    A function that computes predictions for the reservoir areas of the dams
    using the best fit parameters given by the regression algorithm. The
    function then returns the reservoir areas as dataframe.
    '''
    # The path to the file containing the best fit parameters for the model.
    # This shouldn't be hardcoded.
    theta_path = r"C:\Users\Desktop\Downloads\theta_values.txt"
    # Save the theta values in a pandas dataframe.
    theta = pd.read_csv(theta_path, sep='\t', header=None, names=['theta_vals'])
    
    # Get the examples with elevations from the get_elevation function.
    examples = prepare_examples()

    # Create the design matrix.
    design_mtx = pd.concat([np.log(examples['Elevation']),
                            np.log(examples['Capacity'])], axis=1)
    # Add the column of ones at the beginning of the design matrix.
    design_mtx.insert(0, 'Ones', np.ones((len(design_mtx), 1)))
    # Compute the reservoir area predictions using the design matrix and the
    # theta vector.
    area_predictions = np.dot(design_mtx.to_numpy(), theta.to_numpy())
    # Create a new dataframe containing the area predictions and the dam names.
    area_predictions = pd.DataFrame(data=np.exp(area_predictions),
                                    columns=['Reservoir Area'])
    area_predictions.insert(0, 'Name', examples['Name'])
    
    return area_predictions
