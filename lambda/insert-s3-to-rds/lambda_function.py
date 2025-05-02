import boto3
import csv
import psycopg2
import os
from io import StringIO

# Set DB connection parameters
host = os.getenv('DB_HOST')
dbname = os.getenv('DB_NAME')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
port = int(os.getenv('DB_PORT'))

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Extract bucket and object key from event
    bucket = event['Records'][0]['s3']['bucket']['name']
    print(f"Bucket: {bucket}")
    key = event['Records'][0]['s3']['object']['key']
    print(f"Key: {key}")

    # Download file from S3
    response = s3_client.get_object(Bucket=bucket, Key=key)
    print(f"Response: {response}")
    content = response['Body'].read().decode('utf-8')
    print(f"Content: {content}")
    csv_reader = csv.reader(StringIO(content))
    
    # Skip header
    next(csv_reader)

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=host,
        dbname=dbname,
        user=user,
        password=password,
        port=port
    )
    cur = conn.cursor()
    print(f"Cursor: {cur}")
    # Insert data
    for row in csv_reader:
        cur.execute(
            "INSERT INTO users (ID, Name, Age, City) VALUES (%s, %s, %s, %s)",
            (int(row[0]), row[1], int(row[2]), row[3])
        )
    
    conn.commit()
    cur.close()
    conn.close()
    
    return {
        'statusCode': 200,
        'body': f'Data from {key} inserted into database'
    }

