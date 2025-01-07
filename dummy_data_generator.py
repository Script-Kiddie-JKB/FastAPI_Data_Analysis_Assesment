import random
import csv
import os

def generate_dummy_data(rows):
    data = []
    for i in range(rows):
        data.append({
            "id": i + 1,
            "name": f"Person {i + 1}",
            "age": random.randint(20, 69),
            "height": round(random.uniform(1.5, 2.0), 2),
            "weight": round(random.uniform(50, 90), 1),
            "income": random.randint(10000, 99999)
        })
    return data

def create_dummy_csv(rows=20, filename='dummy_data.csv'):
    data = generate_dummy_data(rows)
    
    os.makedirs('data', exist_ok=True)
    
    file_path = os.path.join('data', filename)
    
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ["id", "name", "age", "height", "weight", "income"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    
    return file_path

