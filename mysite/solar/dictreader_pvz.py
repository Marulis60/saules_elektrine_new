import csv
import numpy as np
import pandas as pd

birza_csv = pd.read_csv('birza.csv', encoding="UTF-8")
# print(birza_csv)
# print(type(birza_csv))
birza_py=birza_csv.to_numpy()
for row in birza_py:
    print(row)

