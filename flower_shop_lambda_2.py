import boto3
import json
import uuid
from custom_encoder import Customer_Encoder
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# DynamoDB Tables Information
flower_inventory_table_name = 'flower_inventory'
flower_sales_table_name = 'flower_sales'
flower_purchases_table_name = 'flower_purchases'
dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')
inventory_table = dynamodb.Table(flower_inventory_table_name)
sales_table = dynamodb.Table(flower_sales_table_name)
purchase_table = dynamodb.Table(flower_purchases_table_name)

get_method = 'GET'
post_method = 'POST'
delete_method = 'DELETE'
put_method = 'PUT'
health_path = '/health' # health of the API
flower_path = '/flower'
flowers_path = '/flowers'
sale_path = '/sale'
purchase_path = '/purchase'

def lambda_handler(event, context):
    logger.info(event)
    http_method = event['httpMethod']
    path = event['path']

    # health api endpoint
    if http_method == get_method and path == health_path:
        response = build_response(200)
    
    

def build_response(status_code, body=None):
    response = {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    if body is not None:
        response['body'] = json.dumps(body, cls=Customer_Encoder)
    return response