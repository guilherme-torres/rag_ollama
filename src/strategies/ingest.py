from typing import List
from abc import ABC, abstractmethod

class IngestStragety(ABC):

    @abstractmethod
    def load_documents(self, dataset_path: str) -> List[str]:
        pass

    @abstractmethod
    def sanitize(self, documents: List[str]) -> List[str]:
        pass

    @abstractmethod
    def get_chunks(self, documents: List[str]) -> List[str]:
        pass