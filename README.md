# User-Invoice ETL Pipeline
## Author: Jayden Lee

This repository shows cross-platform ETL/ELT Data Pipeline Architecture that transfers processed data from client machine to DynamoDB Table and S3 bucket.

### Table of Contents
* [Data Pipeline](#data-pipeline)
* [Development Steps](#development-steps)

### Data Pipeline
- Designed pipeline collects, transforms, and loads data from local machine to AWS cloud environment
- Two different *mock data* sources: Invoice data and Users data
    - Each record in Invoice data([Source](https://www.kaggle.com/datasets/tunguz/online-retail?resource=download)) stores details of each item purchased in the order, such as invoice number of order, stockcode of purchased item, buyer's name, ..etc
        - Hence, no UNIQUENESS is enforced as single order can contain multiple items, leading to duplicate order number, buyer's name, invoice date, ..etc
    
    - Each record in Users data represents user input data collected from feature flag(A/B testing) survey application; not all fields were required to be filled by answerers
        - UNIQUENESS is enforced with UserId field
        - Records can be in varying dimensionality; some records can contain more attributes than others

### Development Steps
1. I first created AWS REST API Endpoint Resouce as a front door URL to receive data that flows into AWS environment
    - ex) I created `/jlee_endpoint` Resource and assigned POST Method endpoint

2. Configured Lambda function that receives data POST into API Endpoint and relays it into Kinesis Data Stream
    - ex) I named Lambda function here: `endpointToKinesis`
    - Data POST'd to API Endpoint(`/jlee_endpoint`) --> AWS Lambda(`endpointToKinesis`) --> Kinesis Data Stream

3. Updated Execution role of Lambda function to enable WRITE to Kinesis Data Stream
    - Execution role policies I attached is found: `path/to/execution role policy`

4. Configured AWS Kinesis Data Stream for trigger-based transferring of data from Endpoint to subsequent processing
    - ex) I named my Kinesis Data Stream here: `UserStream`
    - API Endpoint(`/jlee_endpoint`) --> AWS Lambda(`endpointToKinesis`) --> Kinesis Data Stream(`UserStream`)

5. Configured Lambda function that moves stream data from Kinesis to target storage
    - Script can be found: `scripts/lambda_function_kinesisToStorage.py`
    - Loads User data into DynamoDB Table & Invoice data into S3 bucket