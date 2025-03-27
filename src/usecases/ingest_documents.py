from typing import List, Union
from src.strategies.ingest import IngestStragety

class IngestDocumentsUseCase:

    def __init__(self, strategy: IngestStragety):
        self.__strategy = strategy

    def execute(self, documents: Union[List, None] = None, dataset_path: Union[str, None] = None) -> Union[List[str], List]:
        texts, ids = self.__strategy.load_documents(documents=documents)
        sanitized_documents = self.__strategy.sanitize(texts)
        return sanitized_documents, ids