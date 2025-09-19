import base64
import boto3
from datetime import datetime
from zoneinfo import ZoneInfo

s3Client = boto3.client('s3')

# Converting datetime object to string
dateTimeObj = datetime.now(tz=ZoneInfo("America/Los_Angeles"))
dtStr = dateTimeObj.strftime("%b %d %Y-%I%M%S%p")

def lambda_handler(event, context):
    kinesisRecords = list() # List of records to store as individual item 
    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        # If TypeError sequence item 0: expected str instance, bytes found, need to encode to UTF-8 first(see comment below))
        payload = (
            base64.b64decode(record['kinesis']['data']). # Kinesis data stream comes encoded; decode using `base64` which returns decoded data in bytes
            decode('utf-8') # Decode bytes into string
        )

        # Append each record to a list
        kinesisRecords.append(payload)

    # Make a string out of the list. Backslash n for new line in the s3 file
    dataStream = '\n'.join(kinesisRecords)

    # Put the file into the s3 bucket
    _ = s3Client.put_object(
        Body=dataStream, 
        Bucket='jlee-kinesis-target-bucket', 
        Key=f'fromKinesis/output-{dtStr}.txt'
    )

    return 'Successfully processed {} records.'.format(len(event['Records']))