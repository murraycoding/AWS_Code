import json
import os
import boto3
import logging
import random
import math
from custom_encoder import Customer_Encoder
from flowers import build_flower_id

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

    # information from API request
    logger.info(event)
    http_method = event['httpMethod']
    path = event['path']
    request_body = json.loads(event['body'])

    # common information for both paths
    transactionId = math.round(random.random()*10000)

    # initial information for "total" flower information
    total_flowers = 0
    total_flower_types = 0
    total_price = 0

    # flower loop will run for both paths
    for flower in request_body:
        total_flower_types += 1
        total_flowers += flower['quantity']
        total_price += flower['quantity'] * flower['price']

        # generates flower_id based on the flower information in the request body
        flower_id = build_flower_id(request_body = flower)


    # makes sure the combination of method and path is supported
    if http_method == PUT_METHOD and path == PURCHASE_PATH:

        # writes the summary information to the transaction table
        transaction_response = write_to_transaction_table(transactionId, total_flower_types, total_flowers, total_price, "purchase")

        # update inventory table
        current_quantity = get_flower_quantity(flower_id)

            # loop over json elements of flowers


    elif http_method == PATCH_METHOD and path == SALE_PATH:
        
        transaction_response = write_to_transaction_table(transactionId, total_flower_types, total_flowers, total_price, "sale")
 


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

    return response

def update_inventory_table(flower_id, quantity, sale_purchase):

    response = {}
    # search for the item in the table

    # calculate new total

    # write new information to the table

    # return the response

    return response

def get_flower_quantity(flower_id):

    response = client.get_item(
        TableName = FLOWER_INVENTORY_TABLE_NAME,
        Key = {
            'flower_id'
        }
    )