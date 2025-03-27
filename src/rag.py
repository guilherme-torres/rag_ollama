from typing import List
from .config.chroma_config import ChromaConfig
from .usecases.store_embeddings import StoreEmbeddingsUseCase
from .usecases.retrieve_documents import RetrieveDocumentsUseCase
from .usecases.get_embeddings import GetEmbeddingsUseCase
from .usecases.generate_output import GenerateOutputUseCase
from .usecases.ingest_documents import IngestDocumentsUseCase
from .strategies.llm import LLMStrategy
from .strategies.vector_db import VectorDBStrategy
from .services.html_ingest import HTMLIngest
from .strategies.knowledge_base import KnowledgeBaseStrategy
from .usecases.get_documents_from_source import GetDocumentsFromSourceUseCase

class RAGPipeline:

    def __init__(self, knowledge_base: KnowledgeBaseStrategy, llm: LLMStrategy, embedding_function, vector_db: VectorDBStrategy):
        self.__knowledge_base = knowledge_base
        self.__llm = llm
        self.__embedding_function = embedding_function
        self.__vector_db = vector_db
    

    def ingest(self):
        ingest_documents = IngestDocumentsUseCase(HTMLIngest())
        get_documents_from_source = GetDocumentsFromSourceUseCase(self.__knowledge_base)
        documents = get_documents_from_source.execute()
        sanitized_documents, ids = ingest_documents.execute(documents=documents)
        get_embeddings = GetEmbeddingsUseCase(self.__llm)
        embeddings = get_embeddings.execute(documents=sanitized_documents)
        store_embeddings = StoreEmbeddingsUseCase(self.__vector_db)
        store_embeddings.execute(
            documents=sanitized_documents,
            embeddings=embeddings,
            ids=ids,
            embedding_function=self.__embedding_function,
            collection_name=ChromaConfig().COLLECTION_NAME
        )


    def retrieve(self, query: str) -> List[str]:
        retrieve_documents = RetrieveDocumentsUseCase(self.__vector_db)
        results = retrieve_documents.execute(
            query=query,
            n=3,
            embedding_function=self.__embedding_function,
            collection_name=ChromaConfig().COLLECTION_NAME
        )
        return results


    def generate_response(self, query: str, documents: List[str]):
        generate_output = GenerateOutputUseCase(self.__llm)
        output = generate_output.execute(
            query=query,
            documents=documents
        )
        return output