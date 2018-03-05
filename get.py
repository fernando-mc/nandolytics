import boto3
import decimalencoder
import json
import os
import urllib.parse

dynamodb = boto3.resource('dynamodb')


def get(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # Fetch color from the database
    result = table.get_item(
        Key={
            'siteUrl': urllib.parse.unquote(event['pathParameters']['id'])
        }
    )
    print(result)
    print(urllib.parse.unquote(event['pathParameters']['id']))
    # Create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(
            result['Item'],
            cls=decimalencoder.DecimalEncoder
        )    
    }

    return response
