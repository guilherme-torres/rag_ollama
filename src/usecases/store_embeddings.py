from typing import Union, List
from strategies.vector_db import VectorDBStrategy

class StoreEmbeddingsUseCase:

    def __init__(self, strategy: VectorDBStrategy):
        self.__strategy = strategy

    def execute(self, documents: List[str], embeddings: List, embedding_function = None, collection_name: Union[str, None] = None) -> None:
        self.__strategy.store_embeddings(
            documents=documents,
            embeddings=embeddings,
            embedding_function=embedding_function,
            collection_name=collection_name
        )