import os
from src.utils import OilTerminals

def test_uk_oil_data():
    """Testing UK oil terminal xlsx file"""
    data = OilTerminals()
    locations = data.location_names()
    locations_geojson = data.geojson_data()
    assert locations is not None
    assert locations_geojson is not None

def test_xlsx_csv():
    """Testing xlsx to csv conversion"""
    file_path = "UK-oil-terminals/data/uk_oil_terminals.xlsx"
    csv_file_name = "uk_oil_terminals.csv"
    data = OilTerminals()
    path = data.xlsx_to_csv(file_path,csv_file_name)
    assert os.path.exists(path)