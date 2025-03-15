import os
import chromadb
from chromadb.utils.embedding_functions.ollama_embedding_function import OllamaEmbeddingFunction
from dotenv import load_dotenv

load_dotenv()

class ChromaConfig:
    def __init__(self):
        self.OLLAMA_HOST = os.getenv('OLLAMA_HOST')
        self.MODEL_NAME = os.getenv('MODEL_NAME')
        self.DATASET_PATH = os.getenv('DATASET_PATH')
        self.COLLECTION_NAME = os.getenv('COLLECTION_NAME')
    
    def get_client(self):
        return chromadb.PersistentClient()

    def get_embedding_function(self):
        return OllamaEmbeddingFunction(
            url=f'{self.OLLAMA_HOST}/api/embeddings',
            model_name=self.MODEL_NAME
        )