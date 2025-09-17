import os
from dotenv import load_dotenv

from src import JSONifier

_=load_dotenv()
WORKDIR = os.path.abspath(os.path.dirname(__file__))
DATADIR = os.path.join(WORKDIR, 'data')

if __name__ == '__main__':
    ...