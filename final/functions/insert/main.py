import json
import boto3
from faker import Faker

def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TablaDemo')  # Reemplaza con el nombre de tu tabla DynamoDB
    faker = Faker()

    for i in range(5):
        table.put_item(Item = {"Nombre" : faker.name()})

    return {
        "StatusCode" : 200
    }