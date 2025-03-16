from typing import Union, List
from strategies.vector_db import VectorDBStrategy

class RetrieveDocumentsUseCase:

    def __init__(self, strategy: VectorDBStrategy):
        self.__strategy = strategy

    def execute(self, query: str, n: int, embedding_function = None, collection_name: Union[str, None] = None) -> Union[List[str], None]:
        return self.__strategy.retrieve(
            query=query,
            n=n,
            embedding_function=embedding_function,
            collection_name=collection_name
        )