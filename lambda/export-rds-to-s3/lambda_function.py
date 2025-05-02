import boto3
import psycopg2
import csv
import os
from io import StringIO
from datetime import datetime

# DB Configuration
host = os.getenv('DB_HOST')
dbname = os.getenv('DB_NAME')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
port = int(os.getenv('DB_PORT'))

# S3 Config
S3_BUCKET = 'csv-file-upload-read-project'
EXPORT_PREFIX = 'exports'  # Base folder in S3

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password,
            port=port
        )
        cur = conn.cursor()

        # Query the table
        cur.execute("SELECT ID, Name, Age, City FROM users ORDER BY ID;")
        rows = cur.fetchall()

        # Create CSV in memory
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'Name', 'Age', 'City'])  # Header
        writer.writerows(rows)
        output.seek(0)

        # Create folder path like export/2025-04-29/
        today = datetime.utcnow().strftime('%Y-%m-%d')
        s3_key = f"{EXPORT_PREFIX}/{today}/users.csv"

        # Upload to S3
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=output.getvalue()
        )

        print(f"Exported {len(rows)} rows to s3://{S3_BUCKET}/{s3_key}")

        cur.close()
        conn.close()

        return {'statusCode': 200, 'body': f'Exported {len(rows)} rows to S3'}

    except Exception as e:
        print(f"Error: {str(e)}")
        return {'statusCode': 500, 'body': str(e)}
