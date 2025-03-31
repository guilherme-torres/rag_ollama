import uuid
from typing import Union, List
import chromadb
import ollama
from chromadb import ClientAPI, Collection
from src.config.chroma_config import ChromaConfig
from src.strategies.vector_db import VectorDBStrategy
from src.config.ollama_config import OllamaConfig

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

    def retrieve(
        self,
        query: str,
        n: int,
        embedding_function = None,
        collection_name: Union[str, None] = None
    ) -> Union[List[str], None]:
        client = self.__get_client()
        collection = self.__get_collection(client=client, collection_name=collection_name, embedding_function=embedding_function)
        prompt = f'''
        ## Instrução ##
        De acordo com a pergunta, responda em qual lei ela se encaixa com base nos metadados abaixo.
        Informe a lei exatamente como está escrito nos metadados.
        ## Metadados ##
        lei: LEI COMPLEMENTAR Nº 297
        ementa: Dispõe sobre extinção, por transação judicial, de créditos tributários objeto de execução fiscal movida pelo estado do Piauí.
        data: 29 DE MAIO DE 2024
        -------------------------------
        lei: LEI Nº 4.548
        ementa: Dispõe sobre o Imposto sobre a Propriedade de Veículos Automotores, IPVA.
        data: 29 DE DEZEMBRO DE 1992
        -------------------------------
        lei: LEI Nº 4.261
        ementa: Disciplina o Imposto sobre Transmissão "Causa Mortis" e Doação de quaisquer Bens ou Direitos, previstos na alínea "a", do inciso I, do artigo 155, da Constituição Federal.
        data: 01 DE FEVEREIRO DE 1989
        -------------------------------
        lei: LEI Nº 4.257
        ementa: Disciplina a cobrança do Imposto sobre Operações Relativas à Circulação de Mercadorias e Prestações de Serviços de Transporte Interestadual e Intermunicipal e de Comunicação - ICMS.
        data: 06 de janeiro de 1989
        ## Pergunta ##
        {query}
        lei:
        '''
        output = ollama.generate(
            model=self.config.MODEL_NAME,
            prompt=prompt,
            options={
                'temperature': 0
            }
        )
        print(output.response)
        results = collection.query(
            query_texts=[query],
            n_results=n,
            where={"lei": output.response}
        )
        return results['documents'][0]