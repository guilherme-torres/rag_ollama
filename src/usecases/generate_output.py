from typing import List
from strategies.llm import LLMStrategy

class GenerateOutputUseCase:

    def __init__(self, strategy: LLMStrategy):
        self.__strategy = strategy

    def execute(self, query: str, documents: List[str]) -> str:
        return self.__strategy.generate_output(
            query=query,
            documents=documents
        )