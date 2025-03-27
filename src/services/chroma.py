import uuid
from typing import Union, List
import chromadb
from chromadb import ClientAPI, Collection
from src.config.chroma_config import ChromaConfig
from src.strategies.vector_db import VectorDBStrategy

class ChromaDB(VectorDBStrategy):
    
    def __init__(self, config: ChromaConfig):
        self.config = config
        self.__client = chromadb.PersistentClient(
            path=self.config.CHROMA_PATH
        )

    def __get_client(self):
        return self.__client
    
    def __get_collection(self, client: ClientAPI, collection_name: str, embedding_function) -> Collection:
        return client.get_or_create_collection(
            name=collection_name,
            embedding_function=embedding_function
        )

    def store_embeddings(
        self,
        documents: List[str],
        embeddings: List,
        ids: Union[List[str], None] = None,
        embedding_function = None,
        collection_name: Union[str, None] = None
    ) -> None:
        client = self.__get_client()
        collection = self.__get_collection(client=client, collection_name=collection_name, embedding_function=embedding_function)
        collection.upsert(
            ids=ids if ids is not None else [str(uuid.uuid4()) for _ in embeddings],
            embeddings=embeddings,
            documents=documents
        )

    def retrieve(
        self,
        query: str,
        n: int,
        embedding_function = None,
        collection_name: Union[str, None] = None
    ) -> Union[List[str], None]:
        client = self.__get_client()
        collection = self.__get_collection(client=client, collection_name=collection_name, embedding_function=embedding_function)
        results = collection.query(
            query_texts=[query],
            n_results=n
        )
        return results['documents'][0]