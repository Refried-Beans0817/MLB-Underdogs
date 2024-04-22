import pandas as pd

def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError as e:
        print(f"Error: {e}. Please check if the file path '{file_path}' is correct.")
        return None

def identify_undervalued_players(batting_df, salaries_df):
    # Add your data analysis code here to identify undervalued players
    # For example, calculate player value based on batting statistics and salaries
    merged_df = pd.merge(batting_df, salaries_df, on=['playerID', 'yearID'], how='inner')
    merged_df['AVG'] = merged_df['H'] / merged_df['AB']
    merged_df['PlayerValue'] = merged_df['AVG'] / merged_df['salary']
    undervalued_players = merged_df.sort_values(by='PlayerValue', ascending=False).head(10)
    return undervalued_players

def main():
    # Specify the file paths for your CSV data
    batting_file_path = 'Documents/MLB/Batting.csv'
    pitching_file_path = 'Documents/MLB/Pitching.csv'
    salaries_file_path = 'Documents/MLB/Salaries.csv'
    awards_file_path = 'Documents/MLB/AwardsPlayers.csv'

    # Load CSV files into pandas DataFrames
    batting_df = load_data(batting_file_path)
    pitching_df = load_data(pitching_file_path)
    salaries_df = load_data(salaries_file_path)
    awards_df = load_data(awards_file_path)

    # Display the first few rows of the Batting DataFrame as an example
    if batting_df is not None:
        print("Batting DataFrame:")
        print(batting_df.head())

    # Perform data analysis to identify undervalued players
    if batting_df is not None and salaries_df is not None:
        undervalued_players = identify_undervalued_players(batting_df, salaries_df)
        print("\nTop 10 Undervalued Players (Based on AVG and Salary):")
        print(undervalued_players[['playerID', 'yearID', 'AVG', 'salary', 'PlayerValue']].head(10))

    # Save or display your analysis results here
    # Add code here to save results to a file or display them as needed

if __name__ == "__main__":
    main()
