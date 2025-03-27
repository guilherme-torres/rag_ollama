from typing import List
from elasticsearch import Elasticsearch
from src.strategies.knowledge_base import KnowledgeBaseStrategy
from src.config.elasticsearch_config import ElasticsearchConfig

class ElasticsearchService(KnowledgeBaseStrategy):

    def __init__(self, config: ElasticsearchConfig):
        self.config = config
        self.__client = Elasticsearch(
            hosts=[self.config.ELASTIC_HOST],
            basic_auth=(self.config.ELASTIC_USER, self.config.ELASTIC_PASSWORD)
        )

    
    def get_documents(self) -> List:
        response = self.__client.search(
            index=self.config.INDEX_NAME,
            body={
                'size': 100,
                'query': {
                    'match_all': {}
                }
            }
        )
        return [hit['_source'] for hit in response['hits']['hits']]