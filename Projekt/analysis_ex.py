import matplotlib.pyplot as plt
import pandas as pd


class Analyser:
    # Initialize the Analyser
    def __init__(self, table, figure_save_path):
        self.figure_save_path = figure_save_path
        self.final_table = table
        self.filter_for_years()
   
    # Run the analysis
    def run(self):
        self.visualize_sales_per_countries()
        self.visualize_sales_per_year()
        self.find_first_sold_vehicle()
        self.count_vehicles_sold_with_specific_engines()
        self.vehicles_sold_to_new_zealand_with_om936()
    
    # Reduce the DataFrame to the years 2014 to 2020
    def filter_for_years(self):
        df = self.final_table
        df = df[(df["production_date"] >= pd.to_datetime("2014-01-01")) & (df["production_date"] <= pd.to_datetime("2020-12-31"))]
        self.filtered_table = df
   
    # Which are the top three countries to which we sold the most vehicles between 01.01.2014 and 31.12.2020?
    def visualize_sales_per_countries(self):
        top3 = (self.filtered_table.groupby("country")
              .size()
              .sort_values(ascending=False)
              .head(3)
              .reset_index(name="vehicles_sold"))
        plot = top3.plot.bar(x="country", y="vehicles_sold", legend=False, title="Top 3 Länder nach Fahrzeugverkäufen (2014-2020)")
        plt.tight_layout()
        plt.gcf().set_size_inches(10, 6)
        plt.show()
        
    # In which of these years did we sell the most vehicles overall?
    def visualize_sales_per_year(self):
        top3 = (self.filtered_table.groupby(self.filtered_table["production_date"].dt.year)
              .size()
              .sort_values(ascending=False)
              .head(3)
              .reset_index(name="vehicles_sold"))
        plot = top3.plot.bar(x="production_date", y="vehicles_sold", legend=False, title="Top 3 Jahre nach Fahrzeugverkäufen (2014-2020)")

        plt.tight_layout()
        plt.gcf().set_size_inches(10, 6)
        plt.show()

    #What is the VIN of the first vehicle sold chronologically?
    def find_first_sold_vehicle(self):
        first_vehicle = self.final_table.nsmallest(1, "production_date")
        print("Die FIN des zeitlich ersten verkauften Fahrzeugs ist:", first_vehicle["fin"].values[0])

    #How many vehicles were sold between 01.01.2017 and 01.01.2021 with OM934,OM936, OM470 and OM471 engines?
    def count_vehicles_sold_with_specific_engines(self):
        specific_engines = ["Z5C", "Z5B", "Z5D", "Z5E"]  # Codes for OM934, OM936, OM470 and OM471 engines
        df = self.final_table[(self.final_table["production_date"] >= pd.to_datetime("2017-01-01")) &
                               (self.final_table["production_date"] < pd.to_datetime("2021-01-01"))]
        df = df[df["sales_code_array"].str.contains('|'.join(specific_engines))]
        print(f'Es wurden {df.shape[0]} Fahrzeuge mit den spezifischen Motoren verkauft.')

   #Which vehicles (VIN) were sold to New Zealand between 01.01.2017 and 01.01.2021 and with an OM936 engine?
    def vehicles_sold_to_new_zealand_with_om936(self):
        df = self.final_table[(self.final_table["production_date"] >= pd.to_datetime("2017-01-01")) &
                               (self.final_table["production_date"] < pd.to_datetime("2021-01-01"))]
        df = df[(df["country"] == "New Zealand") & (df["sales_code_array"].str.contains("Z5B"))]
        fins = df["fin"].tolist()
        print("Fahrzeuge (FIN) mit OM936 Motor, die nach Neuseeland verkauft wurden:", fins)
