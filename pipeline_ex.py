from tracemalloc import start
from import_data_ex import DataLoader
import pandas as pd
import datetime


class ETL:
    final_table = pd.DataFrame()  # The final table after all transformations

    def __init__(self, data_specs=None): 
        self.importer = DataLoader(data_specs) 
        self.load_data()


    def run(self):
        self.enhance_raw_data()
        self.create_final_table()
        self.save_final_table()
        return self.final_table

    def save_final_table(self):
        database_path = self.importer.database_config["database_path"]
        # your code here #
        with pd.ExcelWriter(f"{database_path}/final_table.xlsx", engine="xlsxwriter", date_format="DD.MM.YYYY", datetime_format="DD.MM.YYYY",) as writer:
            self.final_table.to_excel(writer, index=False)


    def create_final_table(self):
        self.raw_data_tables["sales_codes"] = self.raw_data_tables["sales_codes"].drop(columns=["Unnamed: 0"]) 
        self.raw_data_tables["vehicle_hash"] = self.raw_data_tables["vehicle_hash"].drop(
            columns=['record_source', 'load_ts', 'Unnamed: 0'])
        # your code here #
        self.final_table = pd.merge(
            self.raw_data_tables["sales_codes"],
            self.raw_data_tables["vehicle_hash"],
            how="inner"
        )
        self.final_table = self.final_table.drop(columns=['h_vehicle_hash'])

    def enhance_raw_data(self):
        self.handle_nans()
        self.handle_invalid_fins()
        self.handle_invalid_dates()

    def handle_invalid_dates(self):
        # your code here #
        start = pd.to_datetime("2000-01-01")
        end = pd.to_datetime("2022-12-31")
        df = self.raw_data_tables["sales_codes"]
        df["production_date"] = pd.to_datetime(df["production_date"], errors='coerce')
        df = df[(df["production_date"] >= start) & (df["production_date"] <= end)]
        self.raw_data_tables["sales_codes"] = df
        

    def handle_invalid_fins(self, num_of_digits_in_fin=17):
        # your code here #
        df = self.raw_data_tables["vehicle_hash"].copy()

        # FIN als echten String behandeln + Whitespace entfernen
        fin = df["fin"].astype("string").str.strip()

        # nur genau 17 Zeichen behalten (NaN fliegt automatisch raus, weil Vergleich -> <NA>)
        df = df[fin.str.len().eq(17)]
        self.raw_data_tables["vehicle_hash"] = df
        

    def handle_nans(self):
        # your code here #
        for key in self.raw_data_tables.keys():
            self.raw_data_tables[key] = self.raw_data_tables[key].dropna()
        


    def load_data(self):
        self.raw_data_tables = self.importer.load_data()
