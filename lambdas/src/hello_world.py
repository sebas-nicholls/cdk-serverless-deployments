import boto3
import json
import os

def lambda_handler(event, context):
    table_name = os.environ["TABLE_NAME"]
    if "AWS_SAM_LOCAL" in os.environ:
        client = boto3.client('dynamodb', endpoint_url="http://dynamodb-local:8000")
    else:
        client = boto3.client('dynamodb')

    response = client.scan(
        TableName=table_name
    )

    return {
        "statusCode": 200,
        "body":"trying Canary 3",
        "headers":{"Content-Type":"application/json"}
    }