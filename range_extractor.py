import csv
from datetime import datetime

# Prompt the user for the range of column 1
begin_value = int(input("Enter the beginning value of the range: "))
end_value = int(input("Enter the end value of the range: "))

# Construct the output file name using the user-entered values
output_file_name = f"cresults_{begin_value}_{end_value}.csv"

# Open the input and output CSV files
with open('calculated_results1901-2022.csv', 'r') as input_file, open(output_file_name, 'w', newline='') as output_file:
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)

    # Iterate over the rows in the input CSV file
    for row in reader:
        # Check if the value of column 1 falls within the specified range
        if begin_value <= int(row[0]) <= end_value:
            # Write the row to the output CSV file
            writer.writerow(row)

with open(output_file_name, 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

# Create a dictionary to store the most recent scores for each team
recent_scores = {}

# Loop through the rows in the original file
for row in data:
    team = row[4]
    date_str = row[2]
    ranking = float(row[8])

    # Parse the date string into a datetime object
    date = datetime.strptime(date_str, '%m-%d-%Y')

    # If this is the first time we've seen this team, add them to the dictionary
    if team not in recent_scores:
        recent_scores[team] = {'date': date, 'ranking': ranking}
    else:
        # If this ranking is more recent than the one we have on record, update the dictionary
        if date > recent_scores[team]['date']:
            recent_scores[team] = {'date': date, 'ranking': ranking}

# Sort the dictionary by score in descending order
sorted_scores = sorted(recent_scores.items(), key=lambda x: x[1]['ranking'], reverse=True)

# Write the sorted scores to a new CSV file
with open(f'rankings_{begin_value}_{end_value}.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Team', 'Date', 'Ranking'])
    for team, score_data in sorted_scores:
        date_str = score_data['date'].strftime('%m-%d-%Y')
        writer.writerow([team, date_str, score_data['ranking']])

# Read in the original CSV file
with open(output_file_name, 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

# Create a dictionary to store the total score and count of tests for each student
rankings = {}

# Loop through the rows in the original file
for row in data:
    team = row[4]
    ranking = float(row[8])

    # If this is the first time we've seen this student, add them to the dictionary
    if team not in rankings:
        rankings[team] = {'total': ranking, 'count': 1}
    else:
        # Add the score to the student's total and increment the count
        rankings[team]['total'] += ranking
        rankings[team]['count'] += 1

# Calculate the average score for each student
average_rankings = {}
for team, ranking_data in rankings.items():
    average_rankings[team] = ranking_data['total'] / ranking_data['count']

# Sort the dictionary by average score in descending order
sorted_rankings = sorted(average_rankings.items(), key=lambda x: x[1], reverse=True)

# Write the sorted scores to a new CSV file
with open(f'arankings_{begin_value}_{end_value}.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Team', 'Average Ranking'])
    for team, average_rankings in sorted_rankings:
        writer.writerow([team, average_rankings])