import csv
import json
import requests
import pandas as pd
import os

# Prompt the user to enter the initial year and number of years of data to download
INITIAL_YEAR = int(input("Enter the initial year: "))
NUM_YEARS = int(input("Enter the number of years of data to download: "))

# Set the API key
API_KEY = "qOlAwqVbEVaTjxWqigYKgjGefmcfYU5RFSl8/uIlmEcfVDsDSvvdKvBQQbJDij9H"

# Set the seasonType and division parameters
SEASON_TYPE = "both"
DIVISION = "FBS"

# Set the output file names
csv_filename = f"cfbresults.csv"

# Use a loop to download the JSON files and append them to the CSV file
with open(csv_filename, mode='w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(
        ['season', 'season_type', 'start_date', 'neutral_site', 'home_team', 'home_points', 'away_team', 'away_points'])
    for i in range(NUM_YEARS):
        # Set the year parameter
        year = INITIAL_YEAR + i

        # Set the URL and output file
        url = f"https://api.collegefootballdata.com/games?year={year}&seasonType={SEASON_TYPE}&division={DIVISION}"
        json_filename = f"games_{year}_{SEASON_TYPE}_{DIVISION}.json"

        # Download the JSON file
        print(f"Downloading {json_filename}...")
        headers = {"Authorization": f"bearer {API_KEY}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Write the JSON data to a file
        with open(json_filename, mode='w') as jsonfile:
            json.dump(response.json(), jsonfile, indent=2)

        # Convert the JSON file to CSV and append the data to the output file
        with open(json_filename) as jsonfile:
            data = json.load(jsonfile)
            for game in data:
                csv_writer.writerow(
                    [game['season'], game['season_type'], game['start_date'], game['neutral_site'], game['home_team'],
                     game['home_points'], game['away_team'], game['away_points']])

        # Clean up the temporary files
        os.remove(json_filename)

# Sort the final CSV file by start_date in ascending order
print(f"Sorting {csv_filename} by start_date...")
df = pd.read_csv(csv_filename)
df = df.sort_values('start_date')
df.to_csv(csv_filename, index=False)

print("Done!")
