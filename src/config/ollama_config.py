import os
from dotenv import load_dotenv

load_dotenv()

class OllamaConfig:
    def __init__(self):
        self.OLLAMA_HOST = os.getenv('OLLAMA_HOST')
        self.MODEL_NAME = os.getenv('MODEL_NAME')
        self.MODEL_TEMPERATURE = 0