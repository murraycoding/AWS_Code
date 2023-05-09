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
client = boto3.client('dynamodb')

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

    # flowers end point
    elif http_method == get_method and path == flowers_path:
        print('DEBUG: The API is getting information on all of the flowers')
        response = get_flowers()

    # sale endpoint
    elif http_method == post_method and path == sale_path:
        print("DEBUG: The API is making a sale to a customer")
        request_body = json.loads(event['body'])
        response = make_sale(request_body)

    # purchase endpoint
    elif http_method == post_method and path == purchase_path:
        print("DEBUG: The API is making a purchase of flowers to add to the inventory")
        request_body = json.loads(event['body'])
        response = make_puchase(request_body)

    # flower end point
    elif http_method == get_method and path == flower_path:
        print('DEBUG: Lambda hits the get_flower')
        request_body = json.loads(event['body'])
        flower_id = build_flower_id(request_body)
        response = get_flower(flower_id)
    elif http_method == delete_method and path == flower_path:
        print('DEBUG: Lmabda hits the delete flower method')
        request_body = json.loads(event['body'])
        flower_id = build_flower_id(request_body)
        response = remove_flower(flower_id)
    elif http_method == post_method and path == flower_path:
        print("DEBUG: The API is creating a new flower.")
        request_body = json.loads(event['body'])
        flower_id = build_flower_id(request_body)
        response = add_flower(flower_id, request_body)
    elif http_method == put_method and path == flower_path:
        print("DEBUG: The API is editing a flower.")
        request_body = json.loads(event['body'])
        flower_id = build_flower_id(request_body)
        response = update_flower(flower_id, request_body)
    else:
        response = build_response(404, "Error")
    
    return response


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

def build_flower_id(request_body):
    try:
        flower_name = request_body['name']
        flower_color = request_body['color']
        return str(f'{flower_color}_{flower_name}')

    except:
        return None

def get_flower(flower_id):
    try:
        print(isinstance(flower_id,str))
        print(isinstance(flower_id,dict))
        response = client.get_item(
            TableName = flower_inventory_table_name,
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

        return build_response(200,body)
    except:
        logger.exception("Cannot find flower information.")
    

def remove_flower(flower_id):
    try:
        response = client.delete_item(
            TableName = flower_inventory_table_name,
            Key = {
                'flower_id': {
                    'S': flower_id
                }
            }
        )

        body = {
            'Operation': 'Remove Flower',
            'Message': 'Success'
        }

        return build_response(200, body)
    except:
        logger.exception("Can't remove the flower")

def add_flower(flower_id, request_body):
    try:
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
    

def update_flower(flower_id, request_body):
    try:
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
        response = client.scan(
            TableName = flower_inventory_table_name,
            ExpressionAttributeNames = {
                '#N': 'name',
                '#C': 'color'
            },
            ProjectionExpression = '#N, #C'
        )
        result = response['Items']

        while 'LastEvaluatedKey' in response:
            response = client.scan(
                TableName = flower_inventory_table_name,
                ExclusiveStartKey = response['LastEvaluatedKey'],
                ExpressionAttributeNames = {
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
        print("There is a mistake there")
        return None


def make_sale(request_body):
    pass

def make_puchase(request_body):
    # separates out each item
    for item in request_body['Items']:
        flower_id = build_flower_id(item)
        print(f'Flower ID = {flower_id}')

        # API will try to get the flower
        try:
            response = client.get_item(
                Key = {
                    'flower_id': {
                        'S': flower_id
                    }
                }
            )

            # if the flower already exists, keep the information and add the quantity
            update_response = update_flower(
                flower_id = flower_id,
                request_body = {
                    'name': item['name'],
                    'color': item['color'],
                    'price': response['Item']['price'],
                    'quantity': str(int(response['Item']['quantity']) + int(item['quantity'])) 
                }
            )

        # flower does not exist, need to make a new table entry - price = 0
        except:
            response = add_flower(
                flower_id = flower_id,
                request_body = {
                    'name': item['name'],
                    'color': item['color'],
                    'price': '0',
                    'quantity': item['quantity']
                }
            )

    body = {
        'Operation': 'Purchase',
        'Message': 'Success',
    }
    
    return build_response(200, body)

