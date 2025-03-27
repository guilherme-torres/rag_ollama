from typing import List, Union
from src.strategies.ingest import IngestStragety

class IngestDocumentsUseCase:

    def __init__(self, strategy: IngestStragety):
        self.__strategy = strategy

    def execute(self, documents: Union[List, None] = None, path: Union[str, None] = None) -> Union[List[str], List]:
        texts = self.__strategy.load_documents(documents=documents, path=path)
        sanitized_documents = self.__strategy.sanitize(texts)
        chunks = self.__strategy.get_chunks(sanitized_documents)
        return chunks