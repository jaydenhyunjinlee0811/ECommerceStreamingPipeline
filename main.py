import os
import requests
from dotenv import load_dotenv

from src import JSONifier

_=load_dotenv()
WORKDIR = os.path.abspath(os.path.dirname(__file__))
DATADIR = os.path.join(WORKDIR, 'data')

if __name__ == '__main__':
    # jsonPayload = JSONifier.run(
    #     sourceFp=os.path.join(DATADIR, 'sample.csv')
    # )

    # Dev
    jsonPayload = JSONifier.run(
        sourceFp=os.path.join(DATADIR, 'sample.csv')
    )
    for payload in jsonPayload:
        response = requests.post(
            url=os.environ.get('POST_ENDPOINT'),
            json=payload
        )