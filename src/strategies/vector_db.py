from typing import Union, List
from abc import ABC, abstractmethod

class VectorDBStrategy(ABC):

    @abstractmethod
    def store_embeddings(
        self,
        documents: List[str],
        embeddings: List,
        metadata: Union[List, None] = None,
        ids: Union[List[str], None] = None,
        embedding_function = None,
        collection_name: Union[str, None] = None
    ) -> None:
        pass

    @abstractmethod
    def retrieve(
        self,
        query: str,
        n: int,
        embedding_function = None,
        collection_name: Union[str, None] = None
    ) -> Union[List[str], None]:
        pass