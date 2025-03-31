from typing import List, Union
from abc import ABC, abstractmethod

class IngestStragety(ABC):

    @abstractmethod
    def load_documents(self, documents: Union[List, None] = None, path: Union[str, None] = None) -> List:
        pass

    @abstractmethod
    def sanitize(self, documents: List) -> List:
        pass

    @abstractmethod
    def get_chunks(self, documents: List) -> List:
        pass