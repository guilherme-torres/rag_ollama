import os
from dotenv import load_dotenv

load_dotenv()

class ChromaConfig:
    def __init__(self):
        self.DATASET_PATH = os.getenv('DATASET_PATH')
        self.COLLECTION_NAME = os.getenv('COLLECTION_NAME')
        self.CHROMA_PATH = os.getenv('CHROMA_PATH')