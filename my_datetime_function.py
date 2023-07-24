import boto3
import json
import uuid
import logging
from datetime import date

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# main function for the lambda function
def lambda_handler(event, context):
    logger.info(event)
    logger.info(context)

    result = "The function has completed!"

    return result