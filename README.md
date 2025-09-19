# AWS Pipeline Development Self-Guided Project
## Author: Jayden Lee

This repository contains historical e-commerce data from [Kaggle](https://www.kaggle.com/datasets/tunguz/online-retail?resource=download). With this as a source,this repository shows configuration of cross-platform ETL/ELT pipelines hosted on AWS platform

### Table of Contents
* [Data Pipeline](#data-pipeline)
* [Development Steps](#development-steps)

### Data Pipeline
- Designed pipeline moves data from local client machine to cloud environment(AWS)

### Development Steps
1. I first created AWS API Endpoint Resouce as a front door URL to receive data that flows into AWS environment
    - ex) I created `/jlee_endpoint` Resource and assigned POST Method endpoint
2. Configured Lambda function that receives data POST into API Endpoint and relays it into Kinesis Data Stream
    - ex) I named Lambda function here: `endpointToKinesis`
    - Data POST'd to API Endpoint(`/jlee_endpoint`) --> AWS Lambda(`endpointToKinesis`) --> Kinesis Data Stream

3. Updated Execution role of Lambda function to enable WRITE to Kinesis Data Stream
    - Execution role policies I attached is found: `path/to/execution role policy`

3. Configured AWS Kinesis Data Stream to receive data being relayed from Lambda
    - ex) I named my Kinesis Data Stream hereL `UserStream`
    - API Endpoint(`/jlee_endpoint`) --> AWS Lambda(`endpointToKinesis`) --> Kinesis Data Stream(`UserStream`)

4. Configured Lambda function that consumes stream from Kinesis Data Stream and loads into S3
    - I named Lambda function here: `kinesisToS3`

5. Updated Execution role of Lambda function to enable READ from Kinesis Data Stream and WRITE to landing S3 bucket
    - Execution role policies I attached is found: `path/to/execution role policy`

6. Created landing bucket for all incoming streams from Kinesis
    - I named my bucket here: `jlee-kinesis-target-bucket`

7. 