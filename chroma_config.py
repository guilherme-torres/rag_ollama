import chromadb
from chromadb.utils.embedding_functions.ollama_embedding_function import OllamaEmbeddingFunction

class ChromaConfig:
    def __init__(self):
        self.OLLAMA_HOST = 'http://localhost:11434'
        self.MODEL_NAME = 'llama3.2:3b'
        self.DATASET_PATH = './data.json'
        self.COLLECTION_NAME = 'documentos'
    
    def get_client(self):
        return chromadb.PersistentClient()

    def get_embedding_function(self):
        return OllamaEmbeddingFunction(
            url=f'{self.OLLAMA_HOST}/api/embeddings',
            model_name=self.MODEL_NAME
        )