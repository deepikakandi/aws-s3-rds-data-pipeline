🛠️ AWS S3 to RDS Data Pipeline + Scheduled RDS Export to S3
This project demonstrates an end-to-end serverless data pipeline on AWS using S3, Lambda, PostgreSQL (RDS), CloudWatch Events, and Python.

📌 Project Overview
✅ Upload CSV file to S3 → Automatically ingested into PostgreSQL (RDS) via Lambda
✅ Daily at 10:00 AM UTC → Lambda exports data from RDS and saves it to S3 as a CSV
🔧 AWS Services Used
Amazon S3 – Store input/output CSVs
AWS Lambda – Serverless functions for ingest/export
Amazon RDS (PostgreSQL) – Relational database for data storage
Amazon EventBridge (CloudWatch Events) – Schedule daily exports
IAM Roles – Secure Lambda permissions
🗂️ Project Structure
aws-s3-rds-data-pipeline/ ├── lambda/ │ ├── insert-s3-to-rds/ │ │ └── lambda_function.py │ └── export-rds-to-s3/ │ └── lambda_function.py ├── test_csv/ │ └── small_data.csv └──psycopg2-layer.zip

🚀 Lambda Function Details
1️⃣ insert-s3-to-rds/lambda_function.py
Triggered by S3 incoming/*.csv file uploads. It:

Reads CSV file from S3
Parses rows
Inserts into PostgreSQL table (users)
2️⃣ export-rds-to-s3/lambda_function.py
Triggered by a daily CloudWatch schedule. It:

Connects to PostgreSQL
Extracts all rows
Saves the data as a new CSV file under export/YYYY-MM-DD/users.csv in S3
🔐 Environment Variables for Lambda
Variable	Description
DB_HOST	RDS endpoint
DB_PORT	DB port (usually 5432)
DB_NAME	PostgreSQL DB name
DB_USER	Username
DB_PASS	Password
S3_BUCKET	Your S3 bucket name
EXPORT_PREFIX	Base path for S3 export
📦 psycopg2 Dependency
Since Lambda doesn’t include psycopg2 by default:

Add a Lambda Layer with psycopg2 compiled for AWS Lambda

Or use Serverless Application Repo to deploy psycopg2 as a layer

📅 Scheduled Export Setup
cron(0 10 * * ? *) → 10:00 AM UTC daily
