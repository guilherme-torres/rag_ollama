import uuid
from typing import Union, List
import chromadb
from chromadb import ClientAPI, Collection
from src.config.chroma_config import ChromaConfig
from src.strategies.vector_db import VectorDBStrategy
from src.utils.embedding_function import OllamaEmbeddingFunction

class ChromaDB(VectorDBStrategy):
    
    def __init__(self, config: ChromaConfig):
        self.config = config
        self.__client = chromadb.PersistentClient(
            path=self.config.CHROMA_PATH
        )

    def __get_client(self):
        return self.__client
    
    def __get_collection(self, client: ClientAPI, collection_name: str, embedding_function) -> Collection:
        return client.get_or_create_collection(
            name=collection_name,
            embedding_function=embedding_function
        )

    def store_embeddings(
        self,
        documents: List[str],
        embeddings: List,
        metadata: Union[List, None] = None,
        ids: Union[List[str], None] = None,
        embedding_function = None,
        collection_name: Union[str, None] = None
    ) -> None:
        client = self.__get_client()
        collection = self.__get_collection(client=client, collection_name=collection_name, embedding_function=embedding_function)
        collection.upsert(
            ids=ids if ids is not None else [str(uuid.uuid4()) for _ in embeddings],
            metadatas=metadata,
            embeddings=embeddings,
            documents=documents
        )

    def __route_query(self, query: str):
        categories = {
            "LEI COMPLEMENTAR Nº 297": "Dispõe sobre extinção, por transação judicial, de créditos tributários objeto de execução fiscal movida pelo estado do Piauí.",
            "LEI Nº 4.548": "Dispõe sobre o Imposto sobre a Propriedade de Veículos Automotores, IPVA.",
            "LEI Nº 4.261": "Disciplina o Imposto sobre Transmissão \"Causa Mortis\" e Doação de quaisquer Bens ou Direitos, previstos na alínea \"a\", do inciso I, do artigo 155, da Constituição Federal.",
            "LEI Nº 4.257": "Disciplina a cobrança do Imposto sobre Operações Relativas à Circulação de Mercadorias e Prestações de Serviços de Transporte Interestadual e Intermunicipal e de Comunicação - ICMS.",
            "PGE PI": "Informações sobre a Procuradoria Geral do Estado do Piauí (PGE), Procuradoria Geral de Justiça, dívidas com o Estado do Piauí, dívida ativa."
        }
        client = chromadb.Client()
        collection = self.__get_collection(
            client=client,
            collection_name='categories',
            embedding_function=OllamaEmbeddingFunction()
        )
        collection.upsert(
            ids=list(categories.keys()),
            documents=list(categories.values())
        )
        result = collection.query(
            query_texts=[query],
            n_results=1
        )
        return result["ids"][0]

    def retrieve(
        self,
        query: str,
        n: int,
        embedding_function = None,
        collection_name: Union[str, None] = None
    ) -> Union[List[str], None]:
        categories = self.__route_query(query)
        print(f'{query} -> {categories}')
        client = self.__get_client()
        collection = self.__get_collection(client=client, collection_name=collection_name, embedding_function=embedding_function)
        results = collection.query(
            query_texts=[query],
            n_results=n,
            where={'lei': {'$in': categories}}
        )
        return results['documents'][0]