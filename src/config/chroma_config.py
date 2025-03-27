import os
from dotenv import load_dotenv

load_dotenv()

class ChromaConfig:
    
    def __init__(self):
        self.DATASET_PATH = os.path.join(os.getcwd(), 'documents')
        self.CHROMA_PATH = os.path.join(os.getcwd(), 'chroma')
        self.COLLECTION_NAME = os.getenv('COLLECTION_NAME')