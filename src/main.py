from . import rag
from fastapi import FastAPI
from .utils.embedding_function import OllamaEmbeddingFunction
from .config.ollama_config import OllamaConfig
from .services.ollama import Ollama
from .config.chroma_config import ChromaConfig
from .services.chroma import ChromaDB

app = FastAPI()

llm = Ollama(OllamaConfig())
embedding_function = OllamaEmbeddingFunction()
vector_db = ChromaDB(ChromaConfig())

rag_pipeline = rag.RAGPipeline(
    llm=llm,
    embedding_function=embedding_function,
    vector_db=vector_db
)

@app.post('/ingest')
def ingest():
    rag_pipeline.ingest()


@app.get('/query')
def query(q: str):
    documents = rag_pipeline.retrieve(query=q)
    response = rag_pipeline.generate_response(query=q, documents=documents)
    return {'response': response}