import json

from .InvoiceJSONifier import InvoiceJSONifier

def collectData(
    userSource: str,
    invoiceSource: str
):
    payloads = list()

    # Mock User data 
    # Assume 10 User records flow in at every runtime
    with open(userSource, 'r') as f:
        payloads+=json.load(f)[:100]
        for payload in payloads:
            payload['source'] = 'Users'

    # Invoice data
    payloads+=InvoiceJSONifier.run(sourceFp=invoiceSource)
    return payloads