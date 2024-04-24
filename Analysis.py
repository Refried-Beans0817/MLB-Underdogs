import pandas as pd
import pymysql

def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError as e:
        print(f"Error: {e}. Please check if the file path '{file_path}' is correct.")
        return None

def identify_undervalued_players(batting_df, pitching_df, salaries_df, awards_df):
    # Filter data for years 2015 and onwards
    batting_df = batting_df[batting_df['yearID'] >= 2015]
    pitching_df = pitching_df[pitching_df['yearID'] >= 2015]
    salaries_df = salaries_df[salaries_df['yearID'] >= 2015]
    awards_df = awards_df[awards_df['yearID'] >= 2015]

    # Merge batting, pitching, and salary data with suffixes
    merged_df = pd.merge(batting_df, pitching_df, on=['playerID', 'yearID', 'teamID'], how='inner', suffixes=('_batting', '_pitching'))
    merged_df = pd.merge(merged_df, salaries_df, on=['playerID', 'yearID', 'teamID'], how='inner', suffixes=('_merged', '_salaries'))

    # Calculate batting average (AVG) and player value
    if 'H_batting' in merged_df.columns and 'AB' in merged_df.columns:
        merged_df['AVG'] = merged_df['H_batting'] / merged_df['AB']
        merged_df['PlayerValue'] = merged_df['AVG'] / merged_df['salary']
        
        # Get top 10 undervalued players based on PlayerValue
        undervalued_players = merged_df.sort_values(by='PlayerValue', ascending=False).head(10)
        return undervalued_players
    else:
        print("Required columns 'H_batting' or 'AB' not found in the merged DataFrame.")
        return None

def lambda_handler(event, context):
    # Specify the file paths for your CSV data
    batting_file_path = 's3://team3mlbunderdogs/Baseball Databank/Batting.csv'
    pitching_file_path = 's3://team3mlbunderdogs/Baseball Databank/Pitching.csv'
    salaries_file_path = 's3://team3mlbunderdogs/Baseball Databank/Salaries.csv'
    awards_file_path = 's3://team3mlbunderdogs/Baseball Databank/AwardsPlayers.csv'

    # Load CSV files into pandas DataFrames
    batting_df = load_data(batting_file_path)
    pitching_df = load_data(pitching_file_path)
    salaries_df = load_data(salaries_file_path)
    awards_df = load_data(awards_file_path)

    # Perform data analysis to identify undervalued players
    if batting_df is not None and pitching_df is not None and salaries_df is not None and awards_df is not None:
        undervalued_players = identify_undervalued_players(batting_df, pitching_df, salaries_df, awards_df)
        if undervalued_players is not None:
            return {
                'statusCode': 200,
                'body': undervalued_players.to_dict(orient='records')
            }
        else:
            return {
                'statusCode': 500,
                'body': "Failed to identify undervalued players."
            }
    else:
        return {
            'statusCode': 500,
            'body': "Failed to load CSV files."
        }
