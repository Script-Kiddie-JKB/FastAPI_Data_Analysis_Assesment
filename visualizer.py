import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import uuid
import os

class Visualizer:
    def __init__(self, data: pd.DataFrame):
        self.data = data
    
    def create_visualization(self, chart_type: str, columns: list):
        plt.figure(figsize=(10, 6))
        
        if chart_type == "histogram":
            if len(columns) != 1:
                raise ValueError("Histogram requires exactly one column")
            sns.histplot(data=self.data, x=columns[0], kde=True)
        elif chart_type == "scatter":
            if len(columns) != 2:
                raise ValueError("Scatter plot requires exactly two columns")
            sns.scatterplot(data=self.data, x=columns[0], y=columns[1])
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")
        
        plt.title(f"{chart_type.capitalize()} Plot")
        plt.xlabel(columns[0])
        if chart_type == "scatter":
            plt.ylabel(columns[1])
        
        os.makedirs('temp', exist_ok=True)
        
        image_path = os.path.join('temp', f"{uuid.uuid4()}.png")
        plt.savefig(image_path)
        plt.close()
        
        return image_path

