'''
Date 9/17/25 

File: lambda_function.py
Purpose: Front-door AWS Lamdba function integrated with API Gateway to receive POST requests from client applications
'''

import json
import boto3

def lambda_handler(
    event, # Contains request data
    context
):
    method = event['context']['http-method']

    # Received POST request
    if method == "POST":
        body = event['body-json']
        bodyString = json.dumps(body)

        client = boto3.client('kinesis')
        response = client.put_record(
            StreamName='APIData',
            Data= bodyString,
            PartitionKey='string'
        )

        return {
            'statusCode': 200,
            'body': json.dumps('POST request processed successfully!')
        }