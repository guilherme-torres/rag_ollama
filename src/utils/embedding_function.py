from chromadb import Documents, EmbeddingFunction, Embeddings
from src.services.ollama import Ollama
from src.config.ollama_config import OllamaConfig

class OllamaEmbeddingFunction(EmbeddingFunction):

    def __call__(self, input: Documents) -> Embeddings:
        ollama = Ollama(OllamaConfig())
        embeddings = ollama.get_embeddings(input)
        return embeddings