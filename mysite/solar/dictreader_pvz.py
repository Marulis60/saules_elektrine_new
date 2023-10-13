import csv
import numpy as np
import pandas as pd

birza_csv = pd.read_csv('birza.csv', encoding="UTF-8")
# print(birza_csv)
# print(type(birza_csv))
birza_py=birza_csv.to_numpy()
for row in birza_py:
    print(row[1])

# print(birza_py)
# print(birza_py[0][1])
# print(type(birza_py))

# with open('birza.csv', newline='') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         (row['LAIKAS'], row['KAINA'])