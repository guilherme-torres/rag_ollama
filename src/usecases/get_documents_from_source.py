from typing import List
from src.strategies.knowledge_base import KnowledgeBaseStrategy

class GetDocumentsFromSourceUseCase:

    def __init__(self, strategy: KnowledgeBaseStrategy):
        self.__strategy = strategy


    def execute(self) -> List:
        return self.__strategy.get_documents()