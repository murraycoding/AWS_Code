import json
import os
import boto3

client = boto3.client('dynamodb')

def get_flower_information(event, context):
    if event["httpMethod"] != "GET":
        raise Exception(f"Flower and Flowers API endpoints only accept the GET method, you tried: {event.httpMethod}")

    data = client.scan(TableName=os.environ["SAMPLE_TABLE"])
    items = data["Items"]
    response = {
        "statusCode": 200,
        "body": json.dumps(items)
    }

    return response
