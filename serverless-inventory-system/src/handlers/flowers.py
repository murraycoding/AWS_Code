import json
import os
import boto3
import logging
from custom_encoder import Customer_Encoder

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# DyanmoDB table information
db = boto3.resource('dynamodb')
client = boto3.client('dyanmoDB')
FLOWER_INVENTORY_TABLE_NAME = os.environ["INVENTORY_TABLE"]

# methods and paths
GET_METHOD = "GET"
FLOWER_PATH = "/flower"
FLOWERS_PATH = "/flowers"

def get_flower_information(event, context):

    logger.info(event)
    http_method = event['httpMethod']
    path = event['path']

    if http_method != "GET":
        raise Exception(f"Flower and Flowers API endpoints only accept the GET method, you tried: {event.httpMethod}")
    
    # flower endpoint
    if path == FLOWER_PATH:


    data = client.scan(TableName=os.environ["SAMPLE_TABLE"])
    items = data["Items"]
    response = {
        "statusCode": 200,
        "body": json.dumps(items)
    }

    return response

# standardizes output and utilizes custom encoder if the 'Decimal' value is found in the DyanmoDB table
def build_response(status_code, body=None):
    response = {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }

    # adds a body if one is given
    if body is not None:
        response['body']: json.dumps(body, cls=Customer_Encoder)
    
    return response

# builds the id of the flower based on the name and color of it
def build_flower_id(request_body):
    try:
        flower_name = request_body['name']
        flower_color = request_body['color']
        return str(f'{flower_color}_{flower_name}')
    
    except:
        return None
    
# get single flower function
def get_flower_info(flower_id):
    try:
        response = client.get_item(
            TableName = FLOWER_INVENTORY_TABLE_NAME,
            Key = {
                'flower_id': {
                    'S': flower_id
                }
            }
        )

        body = {
            'Operation': 'Get Flower',
            'Message': 'Success',
            'Item': response['Item']
        }

        return build_response(200, body)
    
    except:
        logger.exception("Cannot find flower information.")