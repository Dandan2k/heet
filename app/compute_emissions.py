# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A script that computes CO2 and CH4 emissions for a given dam using its location,
capacity and trophic state.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Created: 28/08/2021
Last modified: 28/08/2021

Author: Daniel-Alexandru Nistor
"""
import numpy as np
# This will be used to get the elevation of the dam.
from srtm import get_data


# A function that returns the climate zone of the dam.
def get_climate_zone(latitude, longitude):
    return 'boreal'


# A function that returns the reservoir area of the dam.
def get_reservoir_area(latitude, longitude, capacity):
    # The file containing the parameter values for the reservoir area regression
    # algorithm.
    theta_file = 'theta_values.txt'
    # Load the parameters.
    theta = np.loadtxt(theta_file)

    # Get the elevation of the dam.
    elevation = get_data().get_elevation(latitude, longitude)
    # Take the log of the elevation and the capacity in order to use the
    # regression model. Construct the feature vector.
    features = [1, np.log(capacity), np.log(elevation)]
    # Compute the reservoir area.
    reservoir_area = np.dot(features, theta)

    return reservoir_area


# A function that returns the CO2 and CH4 emissions:
def get_emissions(latitude, longitude, capacity, age, trophic_state):
    # A dictionary that maps the IPCC climate zones to a emission coefficient
    # for CO2 and CH4. For CH4, we have two values: one for dams older than 20 
    # years, and one for younger ones. For CO2, we assume no emissions for dams
    # over 20 years old.
    climate_emission_factors = {'boreal': ((0, 344.4), (1.5, 3.0)),
                                'cool temperate': ((0, 373.7), (5.9, 9.2)),
                                'warm temperate dry': ((0, 622.9), (16.4, 21.3)),
                                'warm temperate moist': ((0, 535.0), (8.8, 13.9)),
                                'tropical dry/montane': ((0, 1080.9), (30.9, 42.8)),
                                'tropical moist/wet': ((0, 1015.0), (15.4, 27.4))}
    # A dictionary that maps the trophic state to an adjustment factor.
    trophic_state_factors = {'ultra-oligotrophic': 0.7,
                             'oligotrophic': 0.7,
                             'mesotrophic': 3.0,
                             'eutrophic': 10.0,
                             'hypertrophic': 25.0}
    
    # Get the reservoir area.
    reservoir_area = get_reservoir_area(latitude, longitude, capacity)
    # Get the climate zone of the dam.
    climate_zone = get_climate_zone(latitude, longitude)
    # Get the climate emission factors for CO2 and CH4.
    emission_factor_co2, emission_factor_ch4 = climate_emission_factors[climate_zone]
    # Get the trophic state adjustment factor for the dam.
    trophic_factor = trophic_state_factors[trophic_state]
    
    # Used for selecting the appropiate emission factors.
    index = 0 if age > 20 else 1
    # Compute the CO2 emissions. The result will be in tonnes/yr.
    emissions_co2 = reservoir_area * emission_factor_co2[index]
    # Compute the CH4 emissions. The result will be in tonnes/yr.
    emissions_ch4 = (reservoir_area * emission_factor_ch4[index] * 
                     trophic_factor)

    return (emissions_co2, emissions_ch4)


# Testing.
def main():
    print(get_reservoir_area(21.4, 100.33, 66))
    print(get_emissions(21.4, 100.33, 66, 15, 'eutrophic'))


if __name__ == '__main__':
    main()
