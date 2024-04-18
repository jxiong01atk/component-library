import pandas as pd

def load_data():
    excel_file = "Component_Library_Dummy_Data.xlsx"
    return pd.read_excel(excel_file)
