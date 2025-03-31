from typing import List
import ollama
from src.strategies.llm import LLMStrategy
from src.config.ollama_config import OllamaConfig

class Ollama(LLMStrategy):
    
    def __init__(self, config: OllamaConfig):
        self.config = config

    def get_embeddings(self, documents: List[str]) -> List:
        response = ollama.embed(
            model=self.config.MODEL_NAME,
            input=documents
        )
        return response.embeddings

    def generate_output(self, query: str, documents: List[str]) -> str:
        prompt = f'''
        ## Instrução ##
        Você é um assistente especializado em textos jurídicos que deve buscar informações
        nos documentos fornecidos. Informe para o usuário caso não encontre a informação.
        ## Documentos ##
        {'\n'.join([f' - {document}' for document in documents])}
        ## Pergunta ##
        {query}
        Resposta:
        '''
        print(prompt)
        output = ollama.generate(
            model=self.config.MODEL_NAME,
            prompt=prompt,
            options={
                'temperature': self.config.MODEL_TEMPERATURE
            }
        )
        return output.response