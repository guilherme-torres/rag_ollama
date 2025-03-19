import json
import base64
from typing import List
from bs4 import BeautifulSoup
from strategies.ingest import IngestStragety

class HTMLIngest(IngestStragety):

    def load_documents(self, dataset_path: str) -> List[str]:
        """Obtém conteúdo dos documentos"""
        texts = []
        try:
            with open(dataset_path, 'r', encoding='utf-8') as dataset_file:
                documents = json.load(dataset_file)
                for document in documents:
                    texts.append(base64.b64decode(document['base64_content']).decode())
        except Exception as e:
            print(f'Erro ao ler arquivo {dataset_path}: {e}')
        return texts


    def sanitize(self, documents: List[str]) -> List[str]:
        """Remove tags html e caracteres indesejados"""
        sanitized_documents: list[str] = []
        for document in documents:
            soup = BeautifulSoup(document, 'html.parser')
            sanitized_documents.append(soup.get_text(separator='\n', strip=True))
        return sanitized_documents
    
    def get_chunks(self, documents: List[str]) -> List[str]:
        """Divide documentos em chunks"""
        pass