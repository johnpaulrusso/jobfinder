from db_setup import dynamodb  # Import the initialized DynamoDB resource
from botocore.exceptions import ClientError

def insert_job_item(job_data):
    table = dynamodb.Table('jobs')
    try:
        response = table.put_item(Item=job_data)
        print("Job item inserted successfully:", response)
    except Exception as e:
        print(f"Error inserting item: {e}")

def job_exists(job_data):
    table = dynamodb.Table('jobs')  
    try:
        response = table.get_item(Key={"id": job_data["id"]})
        return "Item" in response
    except ClientError:
        return False

def get_all_jobs():
    table = dynamodb.Table('jobs')
    try:
        # Scan the table to get all items
        response = table.scan()
        items = response.get("Items", [])
        
        if items:
            return items
        else:
            print("No jobs found in the database.")
            return []
    except ClientError as e:
        print(f"An error occurred: {e.response['Error']['Message']}")
        return []