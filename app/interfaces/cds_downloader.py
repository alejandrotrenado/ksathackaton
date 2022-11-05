import cdsapi
import os
import xarray as xr
from app.configuration import conf as cf

class CDS_downloader():

    def __init__(self,variables:list, start_time:str, end_time:str):
        self.download_variables = variables
        self.start_time = start_time
        self.end_time = end_time
        self.client = cdsapi.Client()
   
    def __create_directory(self):
        try:
            os.mkdir("CopernicusData")
        except:
            pass
    
    def __transform_to_pandas(self):
        data = xr.open_dataset("CopernicusData/copernicus_data.nc")
        data_df = data.to_dataframe()
        data_df = data_df.reset_index(level=[0,1,2,3])
        return data_df

    def __create_query(self):
        args_dict = {"variable":self.download_variables,
                    "model":cf.MODEL,
                    "level":cf.LEVEL,
                    "date": f'{self.start_time}/{self.end_time}',
                    "type":cf.TYPE,
                    "time":cf.TIMES,
                    "leadtime_hour":cf.LEADTIME_HOUR,
                    "format":cf.FORMAT}
        self.__create_directory()
        self.client.retrieve(cf.RETRIEVE_NAME,
                            args_dict,"CopernicusData/copernicus_data.nc")
        return self.__transform_to_pandas
    def run_request(self):
        return self.__create_query()
