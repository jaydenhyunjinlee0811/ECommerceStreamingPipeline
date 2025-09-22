import os
import json
import requests
from dotenv import load_dotenv

from src import collectData

_=load_dotenv()

if __name__ == '__main__':
    # Fetch User Profile data and Invoice data info from host app
    payloads = collectData(
        userSource=os.getenv('USER_SOURCE'),
        invoiceSource=os.getenv('INVOICE_SOURCE')
    )
    
    for payload in payloads:
        print(json.dumps(payload, indent=2))
        # POST to Endpoint
        response = requests.post(
            url=os.environ.get('POST_ENDPOINT'),
            json=payload
        )