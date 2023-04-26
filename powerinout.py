import calcxpower
import csv

with open('cfbresults.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        calcxpower.calculate_points_exchange(*row)
print("Done!")