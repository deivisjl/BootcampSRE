import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TablaDemo')  # Reemplaza con el nombre de tu tabla DynamoDB

    response = table.scan()
    lista = []
    items = response['Items']

    for item in items:
        lista.append({"Nombre":item['Nombre']})

    return json.dumps(lista)