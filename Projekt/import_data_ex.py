import pandas as pd
import json
import os


class DataLoader:
    tables = dict()  

    # Initialize the DataLoader
    def __init__(self, data_specs=None):  
        self.__load_json(json_file_name=data_specs) 
        self.__extract_xlsx_path()
        self.__extract_xlsx_name()

    # Load the JSON configuration file
    def __load_json(self, json_file_name=None): 
        with open(json_file_name) as json_file:
            self.database_config = json.load(json_file)

    # Extract the path to the Excel file
    def __extract_xlsx_path(self):
        self.path_to_excel_file = self.database_config["database_path"]

    # Extract the name of the Excel file
    def __extract_xlsx_name(self):
        self.name_of_excel_file = self.database_config["database_name"]

    # Load data from the specified sheet in the Excel file
    def __load(self, sheet=None):
        df = pd.read_excel(os.path.join(self.path_to_excel_file, self.name_of_excel_file),
                           sheet_name=self.database_config[sheet])
        return df

    # Load the data from the imported tables
    def load_data(self):
        self.tables["sales_codes"] = self.__load("sheet1") 
        self.tables["vehicle_hash"] = self.__load("sheet2")
        self.tables["engines"] = self.__load("sheet3")
        return self.tables
