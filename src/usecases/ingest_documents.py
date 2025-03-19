from typing import List
from strategies.ingest import IngestStragety

class IngestDocumentsUseCase:

    def __init__(self, strategy: IngestStragety):
        self.__strategy = strategy

    def execute(self, dataset_path: str) -> List[str]:
        texts = self.__strategy.load_documents(dataset_path)
        sanitized_texts = self.__strategy.sanitize(texts)
        return sanitized_texts