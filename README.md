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
2. Configured Lambda function with relaying ability for data that comes in to created Endpoint
    - Data received through API Endpoint --> AWS Lambda --> AWS Services

3. Published POST method to created AWS Endpoint and integrated created Lambda function to it
    - Data flown in from Client into AWS Endpoint relays directly over to AWS Lambda

4. Created AWS Kinesis Data flow to receive data being relayed from Lambda