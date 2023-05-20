import os
import time
from math import sqrt
import json
import numpy as np
import pandas as pd
import geopandas as gpd
import geojson
from shapely.wkt import loads
from shapely.geometry import mapping

import logging
import logging.config
logging.config.fileConfig('UK-oil-terminals/logger.ini')

class OilTerminals:
    """Class functions of terminal data for Planet"""
    terminal_file_path = 'UK-oil-terminals/data/uk_oil_terminals.xlsx'
    try:
        assert os.path.exists(terminal_file_path) is True
    except AssertionError:
        logging.debug(f"UK oil terminal cannot be found here : {terminal_file_path}")

    def __init__(self) -> None:
        pass

    def location_names(self):
        """Read the xlsx file
        
            Returns: All the location names in lower case
        """
        self.df = pd.read_excel(
            self.terminal_file_path,
            skiprows = 1)
        self.locations = self.df['Region'].tolist()
        self.locations = [loc.split(',')[0].lower() for loc in self.locations]
        return self.locations

    @staticmethod
    def xlsx_to_csv(file_path:str = None, csv_file_name:str = None):
        """Convert a xlsx file to csv"""
        df = pd.read_excel(file_path, skiprows = 1)
        csv_file_path = os.path.join(os.path.dirname(file_path), csv_file_name)
        df.to_csv(csv_file_path, index = None, header = True)
        return csv_file_path
    
    @staticmethod
    def bounding_box(
            center_lat: np.float64 = None,          
            center_lon: np.float64 = None, 
            half_side: np.int64 = 100, # in Km
            ):
        """
        Function that gives WKT of a polygon from a center lon, lat

        Args:
            center_lat: Centre Latitude
            center_lon: Center Longitude
            half_side: Length from center to side of the bounding box in Km.
        
        Returns:
            Polygon WKT string
        """
        # Sanity check
        assert half_side > 0
        assert center_lat >= -90.0 and center_lat  <= 90.0
        assert center_lon >= -180.0 and center_lon <= 180.0

        # Km to m
        half_side = (half_side*1000)/sqrt(2)

        # Geopandas geo-series
        gs = gpd.GeoSeries(loads(f'POINT({center_lon} {center_lat})'))
        # GeoDataFrame
        gdf = gpd.GeoDataFrame(geometry=gs)
        # Projection
        gdf.crs='EPSG:4326'
        gdf = gdf.to_crs('EPSG:3857')
        res = gdf.buffer(
            distance=half_side,
            cap_style=3,
        )    

        # Get the geom
        geom = res.to_crs('EPSG:4326').iloc[0]
        # Getting Polygon WKT string
        return geom.wkt    

    def geojson_data(self)-> None:
        """Getting GeoJSON bbox for each location
        
        Retruns: Dictionary of Location name and geojson format 
        """
        # Getting all the Lat and Lon
        location_geojson = {}
        lat_lon = list(zip(self.df['Lat'], self.df['Lon']))
        for index, row in self.df.iterrows():
            location = row['Region']
            location = location.split(',')[0].lower()
            # Getting the bounding box coords
            wkt_string = OilTerminals.bounding_box(
                center_lat = lat_lon[index][0],
                center_lon = lat_lon[index][1])
            geojson_string = geojson.dumps(mapping(loads(wkt_string)))
            geojson_dict = json.loads(geojson_string)
            location_geojson[location] = geojson_dict
        return location_geojson

