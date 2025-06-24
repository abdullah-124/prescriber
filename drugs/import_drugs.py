# from . import models
import csv

with open('data.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['name'])
print("Data imported successfully!")