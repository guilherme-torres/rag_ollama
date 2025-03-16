from typing import List
import ollama
from strategies.llm import LLMStrategy
from config.ollama_config import OllamaConfig

class Ollama(LLMStrategy):
    
    def __init__(self, config: OllamaConfig):
        self.config = config

    def get_embeddings(self, documents: List[str]) -> List:
        embeddings = ollama.embed(
            model=self.config.MODEL_NAME,
            input=documents
        )
        return embeddings.embeddings

    def generate_output(self, query: str, documents: List[str]) -> str:
        prompt = f'''
        ## Instrução ##
        Você é um assistente especializado que responde perguntas de forma clara e objetiva 
        com base nos documentos fornecidos. Se a resposta não estiver nos documentos,
        você deve dizer que não encontrou a informação.
        ## Documentos ##
        {'\n'.join([f' - {document}' for document in documents])}
        ## Pergunta ##
        {query}
        Resposta:
        '''
        output = ollama.generate(
            model=self.config.MODEL_NAME,
            prompt=prompt,
            options={
                'temperature': self.config.MODEL_TEMPERATURE
            }
        )
        return output.response