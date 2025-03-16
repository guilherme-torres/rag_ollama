import json
from typing import List
from config.chroma_config import ChromaConfig
from usecases.store_embeddings import StoreEmbeddingsUseCase
from usecases.retrieve_documents import RetrieveDocumentsUseCase
from usecases.get_embeddings import GetEmbeddingsUseCase
from usecases.generate_output import GenerateOutputUseCase
from strategies.llm import LLMStrategy
from strategies.vector_db import VectorDBStrategy

class RAGPipeline:

    def __init__(self, llm: LLMStrategy, embedding_function, vector_db: VectorDBStrategy):
        self.__llm = llm
        self.__embedding_function = embedding_function
        self.__vector_db = vector_db


    def __load_dataset(self, dataset_path):
        chunks = []
        try:
            with open(dataset_path, 'r', encoding='utf-8') as dataset_file:
                documents = json.load(dataset_file)
                for document in documents:
                    chunks.append(document['text'])
        except Exception as e:
            print(f'Erro ao ler arquivo {dataset_path}: {e}')
        return chunks
    

    def ingest(self):
        documents = self.__load_dataset(ChromaConfig().DATASET_PATH)
        get_embeddings = GetEmbeddingsUseCase(self.__llm)
        embeddings = get_embeddings.execute(documents=documents)
        store_embeddings = StoreEmbeddingsUseCase(self.__vector_db)
        store_embeddings.execute(
            documents=documents,
            embeddings=embeddings,
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