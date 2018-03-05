import boto3
import json

dynamodb = boto3.resource('dynamodb')


def record(event, context):
    data = json.loads(event['body'])
    if 'siteUrl' not in data:
        logging.error("Validation Failed")
        raise Exception("siteUrl missing")
        return

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    operation_res = dynamodb.update_item(
        Key={
            'siteUrl':{'S': event['body']['siteUrl']}
        },
        UpdateExpression='ADD siteHits :inc',
        ExpressionAttributeValues={
            ':inc': {'N': '1'}
        },
        ReturnValues="UPDATED_NEW"
    )

    item = {
        event['body']['siteUrl'],
        operation_res['siteHits']
    }

    # Create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response
