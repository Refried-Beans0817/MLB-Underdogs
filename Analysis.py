import pandas as pd

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
    merged_df['AVG'] = merged_df['H'] / merged_df['AB']
    merged_df['PlayerValue'] = merged_df['AVG'] / merged_df['salary']

    # Get top 10 undervalued players based on PlayerValue
    undervalued_players = merged_df.sort_values(by='PlayerValue', ascending=False).head(10)
    return undervalued_players

def main():
    # Specify the file paths for your CSV data
    batting_file_path = 'C:/Users/rmart/Documents/MLB/Batting.csv'
    pitching_file_path = 'C:/Users/rmart/Documents/MLB/Pitching.csv'
    salaries_file_path = 'C:/Users/rmart/Documents/MLB/Salaries.csv'
    awards_file_path = 'C:/Users/rmart/Documents/MLB/AwardsPlayers.csv'

    # Load CSV files into pandas DataFrames
    batting_df = load_data(batting_file_path)
    pitching_df = load_data(pitching_file_path)
    salaries_df = load_data(salaries_file_path)
    awards_df = load_data(awards_file_path)

    # Perform data analysis to identify undervalued players
    if batting_df is not None and pitching_df is not None and salaries_df is not None and awards_df is not None:
        undervalued_players = identify_undervalued_players(batting_df, pitching_df, salaries_df, awards_df)
        print("\nTop 10 Undervalued Players (Based on AVG and Salary) after 2015:")
        print(undervalued_players[['playerID', 'yearID', 'AVG', 'salary', 'PlayerValue']].head(10))

if __name__ == "__main__":
    main()
