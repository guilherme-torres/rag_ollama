from typing import List, Union
from abc import ABC, abstractmethod

class IngestStragety(ABC):

    @abstractmethod
    def load_documents(self, documents: Union[List, None] = None, dataset_path: Union[str, None] = None) -> Union[List[str], List]:
        pass

    @abstractmethod
    def sanitize(self, documents: List[str]) -> List[str]:
        pass

    @abstractmethod
    def get_chunks(self, documents: List[str]) -> List[str]:
        pass