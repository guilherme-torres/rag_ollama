from typing import List
from abc import ABC, abstractmethod

class KnowledgeBaseStrategy(ABC):

    @abstractmethod
    def get_documents(self) -> List:
        pass