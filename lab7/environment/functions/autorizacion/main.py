import json
import boto3
from botocore.exceptions import ClientError
#import base64

def get_secret():
    secret_name = "SecretHeaderApi"
    region_name = "us-east-2"
    
    session = boto3.session.Session()
    
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    
    get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        
    secret = get_secret_value_response['SecretString']
    
    return json.loads(secret)["secret_header"]

def lambda_handler(event, context):
    secret = get_secret()
    
    if event['headers']['authorization'] == secret:
        return {
            "isAuthorized" : True
        }
    else :
        return {
            "isAuthorized" : False
        }