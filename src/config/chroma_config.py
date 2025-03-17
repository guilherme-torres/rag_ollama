import os
from dotenv import load_dotenv

load_dotenv()

class ChromaConfig:
    def __init__(self):
        self.DATASET_PATH = os.path.join(os.getcwd(), os.getenv('DATASET_FILE_NAME'))
        self.CHROMA_PATH = os.path.join(os.getcwd(), os.getenv('CHROMA_DIR_NAME'))
        self.COLLECTION_NAME = os.getenv('COLLECTION_NAME')