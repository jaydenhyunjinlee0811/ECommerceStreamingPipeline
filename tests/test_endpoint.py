import pytest
import os
import requests
from dotenv import load_dotenv

_=load_dotenv()

@pytest.fixture(scope='module')
def postEndpoint():
    return os.environ.get('POST_ENDPOINT')

@pytest.fixture(scope='module')
def payload():
    return {
        "InvoiceNo":536365,
        "StockCode":"84029E",
        "Description":"RED WOOLLY HOTTIE WHITE HEART.",
        "Quantity":6,
        "InvoiceDate":"12/1/2010 8:26",
        "UnitPrice":3.39,
        "CustomerID":17850,
        "Country":"United Kingdom"
    }

def test_post(postEndpoint, payload):
    '''
    Ensure API Endpoint exists prior to making POST request from client
    '''
    response = requests.post(
        url=postEndpoint,
        json=payload
    )

    assert response.status_code == 200