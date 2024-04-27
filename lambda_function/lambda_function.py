import pymysql

def lambda_handler(event, context):
    # Connect to the MySQL database
    try:
        conn = pymysql.connect(
            host='database-1.cn4w2w24e6tn.us-west-1.rds.amazonaws.com',
            user='admin',
            password='masterpassword',
            database='database-1'
        )
        cursor = conn.cursor()

        # Execute the SQL query
        query = """
        SELECT 
            Player_name,
            AVG,
            On_base_Percentage,
            Slugging_Percentage,
            On_base_Plus_Slugging
        FROM 
            baseball_hitting
        ORDER BY 
            AVG + On_base_Percentage + Slugging_Percentage + On_base_Plus_Slugging DESC
        LIMIT 
            10;
        """
        cursor.execute(query)

        # Fetch the results into a DataFrame
        results = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        df = pd.DataFrame(results, columns=columns)

        # Close the database connection
        cursor.close()
        conn.close()

        # Convert DataFrame to JSON
        response = df.to_json(orient='records')
        return {
            'statusCode': 200,
            'body': response
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }
