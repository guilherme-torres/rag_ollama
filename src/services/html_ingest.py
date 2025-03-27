import json
import base64
from typing import List, Union
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.strategies.ingest import IngestStragety

class HTMLIngest(IngestStragety):

    def load_documents(self, documents: Union[List, None] = None, path: Union[str, None] = None) -> Union[List[str], List]:
        """Obtém conteúdo dos documentos"""
        texts = []
        ids = []
        try:
            if documents is not None:
                for document in documents:
                    texts.append(base64.b64decode(document['data']).decode())
                    ids.append(f'{document['numero_processo']}_{document['numero_documento']}_{document['sistema']}')
        except Exception as e:
            print(e)
        return texts, ids


    def sanitize(self, documents: List[str]) -> List[str]:
        """Remove tags html"""
        sanitized_documents: list[str] = []
        for document in documents:
            soup = BeautifulSoup(document, 'html.parser')
            sanitized_documents.append(soup.get_text(separator='\n', strip=True))
        return sanitized_documents
    
    
    def get_chunks(self, documents: List[str]) -> List[str]:
        """Divide documentos em chunks"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=20,
            length_function=len
        )
        chunks = []
        for document in documents:
            chunks.extend(text_splitter.split_text(document))
        return chunks