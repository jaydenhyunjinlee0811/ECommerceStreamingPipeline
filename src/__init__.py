import json

from .InvoiceJSONifier import InvoiceJSONifier

def collectData(
    userSource: str,
    invoiceSource: str
):
    payloads = list()

    # User data 
    with open(userSource, 'r') as f:
        payloads+=json.load(f)[:10]
        for payload in payloads:
            payload['source'] = 'Users'

    # Invoice data
    payloads+=InvoiceJSONifier.run(sourceFp=invoiceSource)
    return payloads