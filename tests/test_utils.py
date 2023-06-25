import os
from src.utils import OilTerminals

def test_uk_oil_data():
    """Testing UK oil terminal xlsx file"""
    data = OilTerminals()
    locations = data.location_names()
    data.location_wkt()
    locations_geojson = data.geojson_data()
    assert locations is not None
    assert locations_geojson is not None