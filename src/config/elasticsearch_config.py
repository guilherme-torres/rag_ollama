import os
from dotenv import load_dotenv

load_dotenv()

class ElasticsearchConfig:

    def __init__(self):
        self.ELASTIC_HOST = os.getenv('ELASTIC_HOST')
        self.ELASTIC_USER = os.getenv('ELASTIC_USER')
        self.ELASTIC_PASSWORD = os.getenv('ELASTIC_PASSWORD')
        self.INDEX_NAME = os.getenv('INDEX_NAME')