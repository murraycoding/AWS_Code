import json
import os
import boto3
import logging
import random
import math
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

    response = {}

    logger.info(event)
    http_method = event['httpMethod']
    path = event['path']
    request_body = json.loads(event['body'])

    # makes sure the combination of method and path is supported
    if http_method == PUT_METHOD and path == PURCHASE_PATH:
        # purchase code here
        transactionId = math.round(random.random()*10000)

        # summary information on purchase
        total_flowers = 0
        total_flower_types = 0
        total_purchase_price = 0

        for flower in request_body:
            total_flower_types += 1
            total_flowers += flower['quantity']
            total_purchase_price += flower['quantity'] * flower['price']

        # writes the summary information to the transaction table
        
        # update inventory table

            # loop over json elements of flowers


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

def write_to_transaction_table(transaction_id, total_flower_types, total_flowers, total_price, sale_puchase = "sale"):

    # writes new item to transaction table
    response = client.update_item(
        TableName = TRANSACTION_TABLE_NAME,
        Key = {
            'trasnaction_id': {
                'S': transaction_id
            }
        },
        ExpressionsAttributeNames = {
            '#F': 'total_flower_types',
            '#T': 'total_flowers',
            '#P': 'total_price',
            '#S': 'sale_purchase'
        },
        ExpressionAttributeValues = {
            ':f': {
                'N': total_flower_types
            },
            ':t': {
                'N': total_flowers
            },
            ':p': {
                'N': total_price
            },
            ':s': {
                'S': sale_puchase
            }
        },
        ReturnValues = 'ALL_NEW',
        UpdateExpression = 'SET #F = :f, #T = :t, #P = :p, #S = :s'
    )