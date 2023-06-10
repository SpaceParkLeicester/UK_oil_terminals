import os
import shutil
import pandas as pd
import geopandas as gpd
from shapely.wkt import loads
from src import OilTerminals

class write_shp_file(OilTerminals):
    """Write data into shape files"""
    def __init__(self) -> None:
        super().__init__()
        super().location_names()
        super().location_wkt()
        super().geojson_data()
    
    def write(self)-> None:
        """Writing the data into shape files"""
        shape_file_path = os.path.join('data', 'shape_files')
        if not os.path.exists(shape_file_path):
            os.makedirs(shape_file_path)
        else:
            files = os.listdir(shape_file_path)
            if len(files) != 0:
                for file in files:
                    shutil.rmtree(
                        os.path.join(shape_file_path, file),
                        ignore_errors = True,
                        onerror = None)
        
        for location_name, polygon_obj in self.location_polygon_wkt.items():
            shape_file_folder = os.path.join(shape_file_path, location_name)
            if not os.path.exists(shape_file_folder):
                os.makedirs(shape_file_folder)
            shape_file = os.path.join(shape_file_folder, f'{location_name}.shp')
            gpd.GeoDataFrame(pd.DataFrame(['p1'], columns = ['geom']),
                             crs = {'init' : 'epsg:4326'},
                             geometry = [loads(polygon_obj)]).to_file(shape_file)

if __name__ == "__main__":
    shp = write_shp_file()
    shp.write()