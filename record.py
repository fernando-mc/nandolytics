import boto3
import json
import os

dynamodb = boto3.client('dynamodb')


def record(event, context):
    print('EVENT:')
    print(event)
    data = json.loads(event['body'])
    if 'siteUrl' not in data:
        logging.error("Validation Failed")
        raise Exception("siteUrl missing")
        return

    operation_res = dynamodb.update_item(
        TableName=os.environ['DYNAMODB_TABLE'],
        Key={
            'siteUrl':{'S': data['siteUrl']}
        },
        UpdateExpression='ADD siteHits :inc',
        ExpressionAttributeValues={
            ':inc': {'N': '1'}
        },
        ReturnValues="UPDATED_NEW"
    )
    
    print(type(operation_res['Attributes']['siteHits']['N']))
    print(operation_res['Attributes']['siteHits']['N'])

    item = {
        "siteUrl": data['siteUrl'],
        "siteHits": operation_res['Attributes']['siteHits']['N']
    }

    # Create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response
