import json
import os
import boto3
import logging
from custom_encoder import Customer_Encoder

logger = logging.getLogger()
logger.setLevel(logging.INFO)

db = boto3.resource('dynamodb')
client = boto3.client('dynamodb')
FLOWER_INVENTORY_TABLE_NAME = os.environ["INVENTORY_TABLE"]
TRANSACTION_TABLE_NAME = os.environ["TRANSACTION_TABLE"]

# methods and paths
PUT_METHOD = "PUT"
PATCH_METHOD = "PATCH"
SALE_PATH = "/sale"
PURCHASE_PATH = "/purchase"

# function to update inventory and record sale
def flower_transaction_func(event, context):

    logger.info(event)
    http_method = event['httpMethod']
    path = event['path']

    # makes sure the combination of method and path is supported
    if http_method == PUT_METHOD and path == PURCHASE_PATH:
        # purchase code here
        next
    elif http_method == PATCH_METHOD and path == SALE_PATH:
        # sale code here
        next
 


    # if event["httpMethod"] != "GET":
    #     raise Exception(f"getAllItems only accept GET method, you tried: {event.httpMethod}")

    # data = client.scan(TableName=os.environ["INVENTORY_TABLE"])
    # items = data["Items"]
    # response = {
    #     "statusCode": 200,
    #     "body": json.dumps(items)
    # }

    return response