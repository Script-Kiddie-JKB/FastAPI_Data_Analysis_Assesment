import pandas as pd
import numpy as np
from io import BytesIO

class DataHandler:
    def __init__(self, file_content: bytes):
        self.df = pd.read_csv(BytesIO(file_content))
    
    def get_summary(self):
        summary = {}
        for column in self.df.columns:
            if column not in ['id', 'name']:  # Skip 'id' and 'name' columns
                column_summary = {
                    "mean": float(self.df[column].mean()) if pd.api.types.is_numeric_dtype(self.df[column]) else None,
                    "median": float(self.df[column].median()) if pd.api.types.is_numeric_dtype(self.df[column]) else None,
                    "std": float(self.df[column].std()) if pd.api.types.is_numeric_dtype(self.df[column]) else None,
                    "dtype": str(self.df[column].dtype)
                }
                summary[column] = column_summary
        return summary
    
    def apply_transformations(self, transformations):
        df_copy = self.df.copy()
        
        if "normalize" in transformations:
            for column in transformations["normalize"]:
                df_copy[column] = (df_copy[column] - df_copy[column].min()) / (df_copy[column].max() - df_copy[column].min())
        
        if "fill_missing" in transformations:
            for column, value in transformations["fill_missing"].items():
                df_copy[column].fillna(value, inplace=True)
        
        return df_copy
    
    def get_data(self):
        return self.df

