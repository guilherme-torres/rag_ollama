import rag
from utils.embedding_function import OllamaEmbeddingFunction
from config.ollama_config import OllamaConfig
from services.ollama import Ollama
from config.chroma_config import ChromaConfig
from services.chroma import ChromaDB


def main():
    llm = Ollama(OllamaConfig())
    embedding_function = OllamaEmbeddingFunction()
    vector_db = ChromaDB(ChromaConfig())


    rag_pipeline = rag.RAGPipeline(
        llm=llm,
        embedding_function=embedding_function,
        vector_db=vector_db
    )

    rag_pipeline.ingest()

    query = 'Quais são os sabores das pizzas?'
    documents = rag_pipeline.retrieve(query=query)
    response = rag_pipeline.generate_response(query=query, documents=documents)
    print(response)


if __name__ == '__main__':
    main()