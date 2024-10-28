from db_setup import dynamodb  # Import the initialized DynamoDB resource

def insert_job_item(job_data):
    table = dynamodb.Table('jobs')
    try:
        response = table.put_item(Item=job_data)
        print("Job item inserted successfully:", response)
    except Exception as e:
        print(f"Error inserting item: {e}")