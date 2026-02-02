import matplotlib.pyplot as plt
import pandas as pd


class Analyser:
    def __init__(self, table, figure_save_path):
        self.figure_save_path = figure_save_path
        self.final_table = table
        self.filter_for_years()

    def run(self):
        self.visualize_sales_per_countries()
        self.visualize_sales_per_year()
        self.find_first_sold_vehicle()
        self.count_vehicles_sold_with_specific_engines()
        self.vehicles_sold_to_new_zealand_with_om936()

    def filter_for_years(self):
        df = self.final_table
        # your code here #
        df = df[(df["production_date"] >= pd.to_datetime("2014-01-01")) & (df["production_date"] <= pd.to_datetime("2020-12-31"))]
        self.filtered_table = df

    def visualize_sales_per_countries(self):
        # your code here #
        # Welches sind die top drei Länder, in die wir zwischen 01.01.2014 und 31.12.2020
        # am meisten Fahrzeuge verkauft haben?
        top3 = (self.filtered_table.groupby("country")
              .size()
              .sort_values(ascending=False)
              .head(3)
              .reset_index(name="vehicles_sold"))
        print(top3)
        plot = top3.plot.bar(x="country", y="vehicles_sold", legend=False, title="Top 3 Länder nach Fahrzeugverkäufen (2014-2020)")
        plt.tight_layout()
        plt.gcf().set_size_inches(10, 6)
        plt.show()
        

    def visualize_sales_per_year(self):
        #In welchem dieser Jahre haben wir insgesamt am meisten Fahrzeuge verkauft?
        top3 = (self.filtered_table.groupby(self.filtered_table["production_date"].dt.year)
              .size()
              .sort_values(ascending=False)
              .head(3)
              .reset_index(name="vehicles_sold"))
        plot = top3.plot.bar(x="production_date", y="vehicles_sold", legend=False, title="Top 3 Jahre nach Fahrzeugverkäufen (2014-2020)")

        plt.tight_layout()
        plt.gcf().set_size_inches(10, 6)
        plt.show()

    #Welche FIN hat das zeitlich erste verkaufte Fahrzeug.
    def find_first_sold_vehicle(self):
        first_vehicle = self.final_table.nsmallest(1, "production_date")
        print("Die FIN des zeitlich ersten verkauften Fahrzeugs ist:", first_vehicle["fin"].values[0])

    #Wie viele Fahrzeuge wurden zwischen 01.01.2017 und 01.01.2021 mit OM934,
    #OM936, OM470 und OM471 Motoren verkauft.
    def count_vehicles_sold_with_specific_engines(self):
        specific_engines = ["Z5C", "Z5B", "Z5D", "Z5E"]  # Codes für OM934, OM936, OM470 und OM471 Motoren
        df = self.final_table[(self.final_table["production_date"] >= pd.to_datetime("2017-01-01")) &
                               (self.final_table["production_date"] < pd.to_datetime("2021-01-01"))]
        df = df[df["sales_code_array"].str.contains('|'.join(specific_engines))]
        print(f'Es wurden {df.shape[0]} Fahrzeuge mit den spezifischen Motoren verkauft.')

   #Welche Fahrzeuge (FIN) wurden zwischen 01.01.2017 und 01.01.2021 und mit
   #OM936 Motor nach Neuseeland verkauft.
    def vehicles_sold_to_new_zealand_with_om936(self):
        df = self.final_table[(self.final_table["production_date"] >= pd.to_datetime("2017-01-01")) &
                               (self.final_table["production_date"] < pd.to_datetime("2021-01-01"))]
        df = df[(df["country"] == "New Zealand") & (df["sales_code_array"].str.contains("Z5B"))]
        fins = df["fin"].tolist()
        print("Fahrzeuge (FIN) mit OM936 Motor, die nach Neuseeland verkauft wurden:", fins)
