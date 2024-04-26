import pandas as pd
import pymysql

def load_data_from_mysql():
    # Establish connection to AWS RDS MySQL database
    connection = pymysql.connect(host='your_db_endpoint',
                                 user='your_username',
                                 password='your_password',
                                 database='your_database_name')
    
    # Define SQL queries to retrieve data from MySQL tables
    batting_query = "SELECT * FROM Batting"
    pitching_query = "SELECT * FROM Pitching"
    salaries_query = "SELECT * FROM Salaries"
    awards_query = "SELECT * FROM AwardsPlayers"
    
    # Fetch data using queries and load into pandas DataFrames
    batting_df = pd.read_sql(batting_query, con=connection)
    pitching_df = pd.read_sql(pitching_query, con=connection)
    salaries_df = pd.read_sql(salaries_query, con=connection)
    awards_df = pd.read_sql(awards_query, con=connection)
    
    # Close database connection
    connection.close()
    
    return batting_df, pitching_df, salaries_df, awards_df

def identify_undervalued_players(batting_df, pitching_df, salaries_df, awards_df):
    # Your existing data processing logic here (filtering, merging, calculations, etc.)
    # Example:
    batting_df = batting_df[batting_df['yearID'] >= 2015]
    pitching_df = pitching_df[pitching_df['yearID'] >= 2015]
    salaries_df = salaries_df[salaries_df['yearID'] >= 2015]
    awards_df = awards_df[awards_df['yearID'] >= 2015]
    
    merged_df = pd.merge(batting_df, pitching_df, on=['playerID', 'yearID', 'teamID'], how='inner', suffixes=('_batting', '_pitching'))
    merged_df = pd.merge(merged_df, salaries_df, on=['playerID', 'yearID', 'teamID'], how='inner', suffixes=('_merged', '_salaries'))
    
    # Calculate player metrics (e.g., AVG, PlayerValue) based on DataFrame columns
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
    # Load data from MySQL into pandas DataFrames
    batting_df, pitching_df, salaries_df, awards_df = load_data_from_mysql()
    
    # Perform analysis to identify undervalued players
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
            'body': "Failed to load data from MySQL."
        }
