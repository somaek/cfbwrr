

def calculate_points_exchange(season, season_type, start_date, neutral_site, home_team, home_points, away_team, away_points):
    try:
        home_points = int(float(home_points))
        away_points = int(float(away_points))
    except ValueError:
        # if either home_points or away_points can't be converted to float,
        # skip the row and return None
        return None
    if neutral_site == "False":
        neutral_site = False
    else:
        neutral_site = True
    from datetime import datetime

    # Define the input string
    input_date = start_date

    # Parse the input string into a datetime object
    dt = datetime.strptime(input_date, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Format the datetime object as a string in the desired format
    start_date = dt.strftime("%m-%d-%Y")

    import csv
    team_found = False
    with open('rankings.csv', 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
    # Find the row for the home team
    for row in rows:
        if row[0] == home_team:
            # get home_ranking
            home_ranking = float(row[1])
            team_found = True

    if not team_found:
        home_ranking = float(70)

    # Find the row for the away team
    team_found = False
    for row in rows:
        if row[0] == away_team:
            # get home_ranking
            away_ranking = float(row[1])
            team_found = True
    if not team_found:
        away_ranking = float(70)

    # Step 1
    if neutral_site:
        a = home_ranking
        b = away_ranking
    else:
        a = float(home_ranking) + 3
        b = away_ranking

    # Step 3
    d = abs(b - a)

    # Step 4
    if home_points > away_points + 15:
        exchange = min((10 + b - a) * 0.15, 3)
    elif home_points > away_points and home_points <= away_points + 15:
        exchange = min((10 + b - a) * 0.1, 2)
    elif home_points == away_points:
        exchange = min(d * 0.1, 1)
    elif home_points < away_points and home_points + 15 >= away_points:
        exchange = min((10 + a - b) * 0.1, 2)
    else:
        exchange = min((10 + a - b) * 0.15, 3)

    if season_type == "postseason":
        exchange = exchange * 2

    exchange = max(0,exchange)

    # Step 5 apply the points exchange
    if home_points > away_points:
        new_home_ranking = home_ranking + exchange
        new_away_ranking = away_ranking - exchange
    elif away_points > home_points:
        new_home_ranking = home_ranking - exchange
        new_away_ranking = away_ranking + exchange
    elif home_points == away_points:
        if a > b:
            new_home_ranking = home_ranking - exchange
            new_away_ranking = away_ranking + exchange
        else:
            new_home_ranking = home_ranking + exchange
            new_away_ranking = away_ranking - exchange


    if neutral_site:
        location = "neutral"
    else:
        location = str("@" + home_team)
    with open('calculated_results.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([season, season_type, start_date, location, home_team, str(home_points) + "-" + str(away_points),
                         away_team, exchange, new_home_ranking])
    with open('calculated_results.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([season, season_type, start_date, location, away_team, str(away_points) + "-" + str(home_points),
                         home_team, exchange, new_away_ranking])
    # Update the rankings
    # Find the row for the home team
    with open('rankings.csv', 'r') as file:
        reader = csv.reader(file)
        rows = [row for row in reader]

    team_found = False
    for row in rows:
        if row[0] == home_team:
            # Update the ranking for the away team
            row[1] = str(new_home_ranking)
            row[2] = start_date
            team_found = True

    if not team_found:
        # Add a new row for the away team
        rows.append([home_team, str(new_home_ranking), start_date])

    with open('rankings.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    # Find the row for the away team
    with open('rankings.csv', 'r') as file:
        reader = csv.reader(file)
        rows = [row for row in reader]

    team_found = False
    for row in rows:
        if row[0] == away_team:
            # Update the ranking for the away team
            row[1] = str(new_away_ranking)
            row[2] = start_date
            team_found = True

    if not team_found:
        # Add a new row for the away team
        rows.append([away_team, str(new_away_ranking), start_date])

    with open('rankings.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    # Sort the rows by the team rankings in descending order
    rows_sorted = sorted(rows, key=lambda row: float(row[1]), reverse=True)

    # Write the sorted rows back to the CSV file
    with open('rankings.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows_sorted)

