import mysql.connector

def lambda_handler(event, context):
    # Establish connection to RDS MySQL database
    connection = mysql.connector.connect(
        host='database-1.cn4w2w24e6tn.us-west-1.rds.amazonaws.com',
        user='admin',
        password='masterpassword',
        database='database-1'
    )
    
    # Execute SQL query to retrieve data
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM baseball_hitting")
    data = cursor.fetchall()
    
    # Process data and generate output
    # (Perform data analysis and generate output JSON)
    
    # Close database connection
    cursor.close()
    connection.close()
    
    return {
        'statusCode': 200,
        'body': {
            'message': 'Data retrieved successfully',
            'data': data
        }
    }
