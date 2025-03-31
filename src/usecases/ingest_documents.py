from typing import List, Union
from src.strategies.ingest import IngestStragety

class IngestDocumentsUseCase:

    def __init__(self, strategy: IngestStragety):
        self.__strategy = strategy

    def execute(self, documents: Union[List, None] = None, path: Union[str, None] = None) -> List:
        data = self.__strategy.load_documents(documents=documents, path=path)
        # sanitized_documents = self.__strategy.sanitize(data)
        chunks = self.__strategy.get_chunks(data)
        return chunks