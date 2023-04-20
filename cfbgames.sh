#!/bin/bash

# Prompt the user to enter the initial year and number of years of data to download
read -p "Enter the initial year: " INITIAL_YEAR
read -p "Enter the number of years of data to download: " NUM_YEARS

# Set the API key
API_KEY="qOlAwqVbEVaTjxWqigYKgjGefmcfYU5RFSl8/uIlmEcfVDsDSvvdKvBQQbJDij9H"

# Set the seasonType and division parameters
SEASON_TYPE="both"
DIVISION="FBS"

# Set the output file names
CSV_FILENAME="games_${INITIAL_YEAR}_to_$((INITIAL_YEAR+NUM_YEARS-1))_${SEASON_TYPE}_${DIVISION}.csv"

# Use a loop to download the JSON files and append them to the CSV file
for (( i=0; i<$NUM_YEARS; i++ ))
do
  # Set the year parameter
  YEAR=$((INITIAL_YEAR+i))
  
  # Set the URL and output file
  URL="https://api.collegefootballdata.com/games?year=$YEAR&seasonType=$SEASON_TYPE&division=$DIVISION"
  JSON_FILENAME="games_${YEAR}_${SEASON_TYPE}_${DIVISION}.json"
  CSV_FILENAME_TMP="games_${YEAR}_${SEASON_TYPE}_${DIVISION}.csv"

  # Download the JSON file
  echo "Downloading $JSON_FILENAME..."
  curl -H "Authorization: bearer $API_KEY" "$URL" -o "$JSON_FILENAME"

  # Convert the JSON file to CSV
  echo "Converting $JSON_FILENAME to $CSV_FILENAME_TMP..."
  jq -r '.[] | [ .season, .season_type, .start_date, .neutral_site, .home_team, .home_points, .away_team, .away_points ] | @csv' "$JSON_FILENAME" > "$CSV_FILENAME_TMP"

  # Append the CSV data to the output file
  if [ -s "$CSV_FILENAME" ]; then
    tail -n +2 "$CSV_FILENAME_TMP" >> "$CSV_FILENAME"
  else
    cat "$CSV_FILENAME_TMP" > "$CSV_FILENAME"
  fi

  # Clean up the temporary files
  rm "$JSON_FILENAME" "$CSV_FILENAME_TMP"
done

# Sort the final CSV file by start_date in ascending order
echo "Sorting $CSV_FILENAME by start_date..."
sort -t ',' -k 3 "$CSV_FILENAME" -o "$CSV_FILENAME"

echo "Done!"

