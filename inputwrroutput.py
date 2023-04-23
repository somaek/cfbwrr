import pointsxcalc
import csv

with open('cfbresults.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        pointsxcalc.calculate_points_exchange(*row)
print("Done!")
