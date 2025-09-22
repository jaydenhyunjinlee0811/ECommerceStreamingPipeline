import json
import base64
import boto3
from io import StringIO
from csv import DictWriter
from datetime import datetime
from zoneinfo import ZoneInfo

def itemizeHelper(val):
    typeMapper = {
        str: 'S',
        int: 'N',
        float: 'N',
        bool: 'BOOL'
    }
    # Flat data types
    if isinstance(val, (str,int,float,bool)):
        return {typeMapper[type(val)]: val}
    elif isinstance(val, list):
        # If each item is unique in the container, put attribute as String Set
        if len(val) == len(set(val)):
            return {'SS': [item for item in val]}
        # If uniqueness is not ensured, ingest as List of String
        else:
            return {'L': [{'S': item} for item in val]}
    elif isinstance(val, dict):
        # If an attribute stores nested structure,
        # recursive run on nested value and transform data into DynamoDB item format
        d = {'M': {}}
        for k,v in val.items():
            d['M'][k] = itemizeHelper(v)

        return d

def lambda_handler(event, context):
    '''
    Users streaming data looks:
    Each Record dictionary in `event['Records']`represents single payload
    {
        'Records': [
            {
                'kinesis': {
                    'kinesisSchemaVersion': '1.0',
                    "partitionKey": "string",
                    "sequenceNumber": "49667190169250944649727830147025001609756339658383425538",
                    "approximateArrivalTimestamp": 1758443180.344
                    "data": "eyJVc2VySWQiOiAidXNlcl8xMDAxIiwgIkVtYWlsIjogIm5pY29sZTAxQHlhaG9vLmNvbSIsICJOYW1lIjogIlN0ZXBoZW4iLCAiUHJlZmVyZW5jZXMiOiB7InRoZW1lIjogImxpZ2h0IiwgIm5vdGlmaWNhdGlvbnMiOiB7ImVtYWlsIjogZmFsc2UsICJzbXMiOiBmYWxzZX19LCAiQm9va21hcmtzIjogWyJkb2M4NzkiLCAiZG9jMzUwIiwgImRvYzU2NiJdLCAic291cmNlIjogIlVzZXJzIn0=",
                }
                "eventSource": "aws:kinesis",
                "eventVersion": "1.0",
                "eventID": "shardId-000000000000:49667190169250944649727830147025001609756339658383425538",
                "eventName": "aws:kinesis:record",
                "invokeIdentityArn": "arn:aws:iam::375810804608:role/service-role/kinesisToStorage-role-ebww3yh4",
                "awsRegion": "us-west-1",
                "eventSourceARN": "arn:aws:kinesis:us-west-1:375810804608:stream/UserStream"
            },
            {
                'kinesis': {
                    'kinesisSchemaVersion': '1.0',
                    'data': 'eyJJbnZvaWNlTm8iOiAiNTM2MzY1IiwgIlNGDSFDSDQ=-...' # Base64 encoded JSON string
                    ...
                }
            },
            ...
        ]
    }
    '''
    batchRecs = list()
    dynamoClient = boto3.client('dynamodb')
    s3Client = boto3.client('s3')
    dtStr = datetime.now(tz=ZoneInfo('America/Los_Angeles')).strftime('%Y%m%d %I%M%p')
    numUsers = numInvoice = 0
    for record in event['Records']:
        # Decode streaming data first
        decodedRecord = (
            base64.b64decode(record['kinesis']['data']). # Decode base64-encoded data into bytes
            decode('utf-8') # Decode bytes into string
        )
        recordD = json.loads(decodedRecord) # Parse JSON string to Python dictionary
        source=recordD.pop('source')

        # Users data get stored in DynamoDB Table
        if source=='Users':
            # Partition key: UserId
            itemD = dict()

            # Attributes 
            # Each user has varying attribute set, each of which stores different data type
            # I've implemented helper function above for precise data type mapping
            for key, val in recordD.items():
                itemD[key] = itemizeHelper(val)

            # WRITE to Dynamodb using `client.put_item()`
            _ = dynamoClient.put_item(
                TableName='Users',
                Item=itemD
            )
            numUsers+=1

        elif source=='Invoice':
            batchRecs.append(recordD)
            numInvoice+=1

    if batchRecs:
        print('Writing out Invoice data')
        dataStream = StringIO()
        writer = DictWriter(
            dataStream,
            fieldnames=['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country']
        )
        _ = writer.writeheader()
        _ = writer.writerows(batchRecs)

        # Put the file into the s3 bucket
        _ = s3Client.put_object(
            Body=dataStream.getvalue(), 
            Bucket='jlee-kinesis-target-bucket', 
            Key=f'fromKinesis/output-{dtStr}.txt'
        )

    return f'Successfully uploaded {numUsers} User records and {numInvoice} invoice data.'