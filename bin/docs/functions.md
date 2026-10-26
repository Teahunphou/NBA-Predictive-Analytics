# Function Documentation

## make_request(endpoint, params=None)

Sends a GET request to TheSportsDB API and returns JSON data.

## find_nba_league()

Searches TheSportsDB for basketball leagues and returns the NBA league information.

## get_nba_teams()

Downloads NBA team information and converts the API response into a pandas DataFrame.

## get_nba_games(league_id)

Downloads NBA games for the selected season and converts them into a pandas DataFrame.

## create_features(games_df)

Creates engineered features including:

- total_points
- score_difference
- home_win

## save_data(teams_df, games_df)

Saves the processed datasets into:

- nba_teams.csv
- nba_games.csv

## main()

Runs the complete NBA ingestion pipeline:

1. Find NBA league
2. Download teams
3. Download games
4. Create features
5. Save data
