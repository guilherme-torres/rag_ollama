import os
import json
from typing import List, Union
from docling.document_converter import DocumentConverter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.strategies.ingest import IngestStragety

class PdfIngest(IngestStragety):

    def load_documents(self, documents: Union[List, None] = None, path: Union[str, None] = None) -> List:
        """Obtém conteúdo dos documentos"""
        data = []
        converter = DocumentConverter()
        groups = os.listdir(path)
        for group in groups:
            metadata = None
            contents = []
            files = [os.path.join(path, group, file_name) for file_name in os.listdir(os.path.join(path, group))]
            for file_path in files:
                if os.path.basename(file_path) == 'metadata.json':
                    with open(file_path, 'r', encoding='utf-8') as metadata_file:
                        metadata = json.load(metadata_file)
                else:
                    result = converter.convert(source=file_path)
                    content = result.document.export_to_markdown(image_placeholder='')
                    contents.append(content)
            data.append({
                'metadata': metadata,
                'contents': contents
            })
        return data
        # texts = []
        # converter = DocumentConverter()
        # results = converter.convert_all(source=[os.path.join(path, file) for file in os.listdir(path)])
        # for result in results:
        #     texts.append(result.document.export_to_markdown())
        # return texts


    def sanitize(self, documents: List) -> List:
        """Sanitiza o conteúdo dos documentos"""
        pass
    
    
    def get_chunks(self, documents: List) -> List:
        """Divide documentos em chunks"""
        text_splitter = RecursiveCharacterTextSplitter(
            separators=['##', '\nArt.']
        )
        data = []
        for document in documents:
            for content in document['contents']:
                chunks = text_splitter.split_text(content)
                for chunk in chunks:
                    data.append({
                        'metadata': document['metadata'],
                        'chunk': chunk
                    })
        return data