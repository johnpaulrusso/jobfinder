import boto3
import os

# Initialize the DynamoDB resource
if os.getenv("ENV") == "production":
    dynamodb = boto3.resource("dynamodb")
else:
    dynamodb = boto3.resource(
        'dynamodb',
        endpoint_url=os.getenv('DYNAMODB_ENDPOINT', 'http://localhost:8000'),
        region_name=os.getenv('AWS_REGION', 'us-east-2'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', 'mock_access_key'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', 'mock_secret_key')
    )

def create_jobs_table():
    """
    Creates the 'jobs' table if it doesn't already exist.
    """
    try:
        # Attempt to describe the table to check if it exists
        dynamodb.Table('jobs').load()
        print("Table 'jobs' already exists.")
    except dynamodb.meta.client.exceptions.ResourceNotFoundException:
        # If the table doesn't exist, create it
        print("Creating 'jobs' table...")
        table = dynamodb.create_table(
            TableName='jobs',
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.wait_until_exists()
        print("Table 'jobs' created successfully.")

# Run this to ensure the table exists at the start
create_jobs_table()