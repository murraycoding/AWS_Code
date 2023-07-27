import json
import os
import boto3

def health_check(event, context):
    if event["httpMethod"] != "GET":
        raise Exception(f"getAllItems only accept GET method, you tried: {event.httpMethod}")
    try:
        response = {
            "statusCode": 200,
            "body": "API is functional"
        }

    except:
        return None

    return response