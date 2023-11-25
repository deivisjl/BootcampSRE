import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TablaDemo')  # Reemplaza con el nombre de tu tabla DynamoDB

    response = table.scan()
    items = response['Items']

    for item in items:
        nombre = item['Nombre']

    return {
        'statusCode': 200,
        'body': f"Hello, {nombre}!"
    }