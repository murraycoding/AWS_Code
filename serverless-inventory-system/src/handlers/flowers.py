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
        flower_id = event['queryStringParameters']['flower_id']
        response = get_flower_info(flower_id)

    if path == FLOWERS_PATH:
        response = get_all_flowers_info()

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

# get information on all flowers
def get_all_flowers_info():
    try:
        response = client.scan(
            TableName = FLOWER_INVENTORY_TABLE_NAME,
            ExpressionAttributeNames = {
                '#N': 'name',
                '#C' : 'color'
            },
            ProjectionExpression = '#N, #C'
        )
        result = response['Items']

        while 'LastEvaluatedKey' in response:
            response = client.scan(
                TableName = FLOWER_INVENTORY_TABLE_NAME,
                ExclusiveStartKey = response['LastEvaluatedKey'],
                ExpressionAttributeName = {
                    '#N': 'name',
                    '#C': 'color'
                },
                ProjectionExpression = '#N, #C'
            )
            result.extend(response['Items'])

        body = {
            'flowers': result
        }

        return build_response(200, body)
    
    except:
        print("There is a mistake here.")
        return None