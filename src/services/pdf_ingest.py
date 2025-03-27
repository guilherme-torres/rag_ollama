import os
from typing import List, Union
from docling.document_converter import DocumentConverter
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from src.strategies.ingest import IngestStragety

class PdfIngest(IngestStragety):

    def load_documents(self, documents: Union[List, None] = None, path: Union[str, None] = None) -> Union[List[str], List]:
        """Obtém conteúdo dos documentos"""
        texts = []
        converter = DocumentConverter()
        results = converter.convert_all(source=[os.path.join(path, file) for file in os.listdir(path)])
        for result in results:
            texts.append(result.document.export_to_markdown())
        return texts


    def sanitize(self, documents: List[str]) -> List[str]:
        """Sanitiza o conteúdo dos documentos"""
        return documents
    
    
    def get_chunks(self, documents: List[str]) -> List[str]:
        """Divide documentos em chunks"""
        text_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.MARKDOWN,
            chunk_size=500,
            chunk_overlap=100
        )
        chunks = []
        for document in documents:
            chunks.extend(text_splitter.split_text(document))
        return chunks