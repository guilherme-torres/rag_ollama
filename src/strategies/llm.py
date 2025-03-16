from typing import List
from abc import ABC, abstractmethod

class LLMStrategy(ABC):
    
    @abstractmethod
    def get_embeddings(self, documents: List[str]) -> List:
        pass

    @abstractmethod
    def generate_output(self, query: str, documents: List[str]) -> str:
        pass