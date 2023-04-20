import csv


def calculate_points_exchange(home_team, away_team, home_points, away_points, neutral_site):
    # Load rankings from CSV file
    with open('rankings.csv', mode='r') as file:
        reader = csv.reader(file)
        rankings = {rows[0]: int(rows[1]) for rows in reader}
    for row in reader:
        rankings[row[0]] = int(row[1])

    if home_team not in rankings:
        rankings[home_team] = 70
        with open('rankings.csv', mode='a') as file:
            writer = csv.writer(file)
            writer.writerow([home_team, rankings[home_team]])

    if away_team not in rankings:
        rankings[away_team] = 70
        with open('rankings.csv', mode='a') as file:
            writer = csv.writer(file)
            writer.writerow([away_team, rankings[away_team]])

    if home_team not in rankings or away_team not in rankings:
        print('One or more teams not found in rankings.csv. Using default ranking of 70.')
    # Set default rankings for new teams
    home_rank = rankings.get(home_team, 70)
    away_rank = rankings.get(away_team, 70)

    # Modify pre-match ranking scores for home and away teams
    home_score = home_rank + 3 if (not neutral_site) and (home_team == home_team) else home_rank
    away_score = away_rank + 3 if (not neutral_site) and (away_team == home_team) else away_rank

    # Calculate difference in pre-match ranking scores
    score_diff = abs(home_score - away_score)

    # Calculate points exchange based on match result
    if home_points > away_points:
        if score_diff >= 16:
            points_exchange = min((10 + away_score - home_score) * 0.15, 3)
        else:
            points_exchange = min((10 + away_score - home_score) * 0.1, 2)
        # Update rankings
        rankings[home_team] += points_exchange
        rankings[away_team] -= points_exchange
    elif home_points < away_points:
        if score_diff >= 16:
            points_exchange = min((10 + home_score - away_score) * 0.15, 3)
        else:
            points_exchange = min((10 + home_score - away_score) * 0.1, 2)
        # Update rankings
        rankings[home_team] -= points_exchange
        rankings[away_team] += points_exchange
    else:
        points_exchange = min(score_diff * 0.1, 1)

    # Update rankings for a tie
    if home_points == away_points:
        rankings[home_team] += points_exchange
        rankings[away_team] += points_exchange

    # Write updated rankings to CSV file
    with open('rankings.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows([[team, rank] for team, rank in rankings.items()])

    return points_exchange
