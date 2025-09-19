import json
import random 
import base64
import boto3

ATTRS_DICT = {
    'GENDER':['M','F'],
    'STATUS': ['single', 'married', 'divorced', 'widowed'],
    'AGE': range(18,70),
    'EMPLOYMENT': ['employed', 'unemployed', 'student', 'retired', 'self-employed', 'part-time', 'contract'],
    'INCOME': ['<20K', '20K-50K', '50K']
}

def lambda_handler(event, context):
    '''
    Here event looks:
    {
        'Records': [
            {
                'kinesis': {
                    'kinesisSchemaVersion': '1.0',
                    'data': 'eyJJbnZvaWNlTm8iOiAiNTM2MzY1IiwgIlN...' # Base64 encoded JSON string
                    ...
                }
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
    client = boto3.client('dynamodb')
    print("Received event: " + json.dumps(event, indent=2))
    for i,record in enumerate(event['Records']):
        # Kinesis data is encoded
        rec = (
            base64.b64decode(record['kinesis']['data']). # Decode base64-encoded data into bytes
            decode('utf-8') # Decode bytes into string
        )

        # JSON string -> Python dictionary
        recordD = json.loads(rec)

        # Customer record
        customerId = str(recordD['CustomerID'])
        customer = { # Define KeyAttribute of inserting record {'keyName': {'dataType': value}}
            'customerId':{
                'S': customerId # 'S' to indicate String data type; 'N' for number
            },
            # 'SortKey': {'N': 123} # Sort key to specify if table has Sort Key
        }

        attr1, attr2 = random.sample(list(ATTRS_DICT.keys()),k=2)
        # WRITE/UPDATE to Dynamodb using `client.update_item()`
        response = client.update_item(
            TableName='Customers', 
            Key=customer,
            UpdateExpression='SET #attr = :val1, #attr2 = :val2',
            ExpressionAttributeNames={
                '#attr': attr1,
                '#attr2': attr2
            },  
            ExpresssionAttributeValues={
                ':val1': {'S': random.choice(ATTRS_DICT[attr1])},
                ':val2': {'S': random.choice(ATTRS_DICT[attr2])}
            },
            returnValues="UPDATED_NEW"
        )
        print(response)

        # Create Inventory Row
        #############################

        # inventory_key = dict()
        # inventory_key.update({'InvoiceNo': {"N": str(dict_record['InvoiceNo'])}})

        # #create export dictionary
        # ex_dynamoRecord = dict()

        # #remove Invoice and Stock code from dynmodb record
        # stock_dict = dict(dict_record)
        # stock_dict.pop('InvoiceNo',None)
        # stock_dict.pop('StockCode',None)

        # #turn the dict into a json
        # stock_json = json.dumps(stock_dict)

        # #create a record (column) for the InvoiceNo
        # #add the stock json to the column with the name of the stock number
        # ex_dynamoRecord.update({str(dict_record['StockCode']): {'Value':{"S":stock_json},"Action":"PUT"}})

        #print(ex_dynamoRecord)
        # response = client.update_item(TableName='Invoices', Key = inventory_key, AttributeUpdates = ex_dynamoRecord)


    return 'Successfully processed {} records.'.format(len(event['Records']))