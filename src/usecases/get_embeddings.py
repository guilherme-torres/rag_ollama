from typing import List
from strategies.llm import LLMStrategy

class GetEmbeddingsUseCase:

    def __init__(self, strategy: LLMStrategy):
        self.__strategy = strategy

    def execute(self, documents: List[str]) -> List:
        return self.__strategy.get_embeddings(documents=documents)