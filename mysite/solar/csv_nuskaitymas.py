import csv

with open("../../birza1005.csv", newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        print(row[0], row[1], row[2])
        # print(', '.join(row))
