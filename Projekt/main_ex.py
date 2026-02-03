from pipeline_ex import ETL
from analysis_ex import Analyser

# Calling up the required functions in the right order

figure_save_path = "C:\\Schule\\Informatik\\Projekt\\"
pipeline = ETL("data_specs.json")
final_table = pipeline.run()
analyser = Analyser(final_table, figure_save_path=figure_save_path)
analyser.run()

