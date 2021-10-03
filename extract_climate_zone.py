# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A script that allows the user to extract the climate zone of a
latitude-longitude pair using an ArcGIS Pro project.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Created: 18/08/2021
Last Updated: 18/08/2021

Author: Daniel-Alexandru Nistor
"""
import fiona
from shapely.geometry import Point, mapping, shape

def get_climate_zone(latitude, longitude):
    # Create a point shapefile using the latitude and longitude. We will use
    # this to check in which climate zone does the point fall into. We will use
    # WGS 1984 as our coordinate reference system.
    # First, create the schema for the point.
    schema = {'geometry': 'Point',
              'properties': {'Name': 'str'}}
    # Create the point object.
    with fiona.open('dam_location.shp', mode='w', driver='ESRI Shapefile',
                    schema=schema, crs='EPSG:4326') as dam: 
        # Create the point data.
        point = Point(latitude, longitude)
        prop = {'Name': 'Dam'}
        # Save the data into the dam object.
        dam.write({'geometry': mapping(point), 'properties': prop})

    # Now open the shapefile containing the climate zones.
    with fiona.open('climate_zones_files/climate_zones.shp') as regions:
        # Open the dam location point.
        with fiona.open('dam_location.shp') as dam:
            point = shape(next(iter(dam))['geometry'])
            for region in regions:
                if point.within(shape(region['geometry'])):
                    print(region['properties']['Temp_Moist'])
                    break

# Testing.
if __name__ == '__main__':
    get_climate_zone(21.4, 100.33)