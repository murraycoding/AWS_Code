import boto3
import json
from custom_encoder import Customer_Encoder
import uuid

# logging packages
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
        print("DEBUG: The API is making a health check.")
        response = build_response(200)

    # flower end point
    elif http_method == get_method and path == flower_path:
        print("DEBUG: The API is getting the information for a single flower.")
        flower_id = event['queryStringParameters']['flower_id']
        response = get_flower(flower_id)
    elif http_method == delete_method and path == flower_path:
        print("DEBUG: The API is deleting a single flower.")
        flower_id = event['queryStringParameters']['flower_id']
        response = remove_flower(flower_id)
    elif http_method == post_method and path == flower_path:
        print("DEBUG: The API is creating a new flower.")
        request_body = json.loads(event['body'])
        response = add_flower(request_body)
    elif http_method == put_method and path == flower_path:
        print("DEBUG: The API is editing a flower.")
        request_body = json.loads(event['body'])
        response = update_flower(request_body)
    
    # flowers end point
    elif http_method == get_method and path == flowers_path:
        print("DEBUG: The API is getting information on all of the flowers.")
        response = get_flowers()
    
    # sale end point
    elif http_method == post_method and path == sale_path:
        print("DEBUG: The API is making a sale request.")
        flower_list = 'put flower list here'
        response = make_sale(flower_list)
    
    # purchase end point
    elif http_method == post_method and path == purchase_path:
        print("DEBUG: The API is making a purchase request.")
        flower_list = 'put flower list here'
        response = make_purchase(flower_list)
    
    else:
        print("DEBUG: None of the path and request conditions were met.")
        response = build_response(404, 'Not Found')
    return response

def get_random_primary_key():
    return uuid.uuid4()

def get_flower(flower_id):
    try:
        response = inventory_table.get_item(
            Key = {
                'flower_id': flower_id
            }
        )
        if 'Item' in response:
            return build_response(200, response['Item'])
        else:
            return build_response(404, {'Message': 'Cannot find the flower.'})

    except:
        logger.exception("Cannot get the flower.")

# function will remove a flower from the inventory regardless of the products in stock
def remove_flower(flower_id): # <== query string parameter
    try:
        response = inventory_table.delete_item(
            Key = {
                'flower_id': flower_id
            },
            ReturnValues = 'ALL_OLD' 
        )

        body = {
            'Message': 'This is a test.'
        }

        return build_response(200, body)
    
    except:
        logger.exception("Can't delete the item.")

# function will add flower listing to inventory
def add_flower(request_body):
    try:
        inventory_table.put_item(Item=request_body)
        # api body to send to client
        body = {
            'Operation': 'Add Flower',
            'Message': 'Success',
            'Item': {
                'flower_id': request_body['flower_id'],
                'name': request_body['name'],
                'color': request_body['color'],
                'price': request_body['price'],
                'quantity': request_body['quantity']
            }
        }

        return build_response(200, body)
    
    except:
        logger.exception("The table cannot be reached to add the flower to.")

def update_flower(request_body):
    try:
        flower_id = request_body['flower_id']
        name = request_body['name']
        color = request_body['color']
        price = request_body['price']
        quantity = request_body['quantity']
        
        # used for debugging
        print(f'Flower ID = {flower_id}')
        print(f'Name = {name}')
        print(f'Color = {color}')
        print(f'Price = {price}')
        print(f'Quantity = {quantity}')
        
        response = client.update_item(
            
        TableName = flower_inventory_table_name,
        
        ExpressionAttributeNames = {
            '#N': 'name',
            '#C': 'color',
            '#P': 'price',
            '#Q': 'quantity'
        },
        ExpressionAttributeValues = {
            ':n': {
                'S': name 
            },
            ':c': {
                'S': color
            },
            ':p': {
                'N': price
            },
            ':q': {
                'N': quantity
            }
        },
        Key = {
            'flower_id': {
                'S': flower_id
            }
        },
        ReturnValues = 'ALL_NEW',
        UpdateExpression = 'SET #N = :n, #C = :c, #P = :p, #Q = :q'
        )
        
        print(response)
        
        body = {
            'Message': 'Still Good!' # update this to include more information
        }
        
        return build_response(200, body)

    except:
        logger.exception("There is a problem here.")
    

def get_flowers():
    try:
        response = inventory_table.scan()
        result = response['Items']

        while 'LastEvaluatedKey' in response:
            response = inventory_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            result.extend(response['Items'])

        body = {
            'flowers': result
        }

        return build_response(200, body)
    
    except:
        logger.exception("Can't get flowers.")

# function will update inventory list and add row to sales table
# will need to return a message if a particular flower is out of stock
def make_sale(flower_list): # this is a bit more complicated - start with make purchase
    pass

# function will update inventory list and add row to purchases table
def make_purchase(flower_list):
    # To-Do 
    # (1) Make a new record in the purchases table
    # (2) Update the inventory to reflect the added purchases
    pass
    

# function to take information from the request and build the response to send to the client
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