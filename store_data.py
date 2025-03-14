import json
from chromadb import ClientAPI
from chroma_config import ChromaConfig

def load_dataset(dataset_path):
    documents = []
    try:
        with open(dataset_path, 'r', encoding='utf-8') as dataset_file:
            documents = json.load(dataset_file)
    except Exception as e:
        print(f'Erro ao ler arquivo {dataset_path}: {e}')
    return documents

def save_data_to_vector_db(client: ClientAPI, collection_name, embedding_function, documents):
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_function
    )
    collection.upsert(
        documents=[document['text'] for document in documents],
        ids=[document['id'] for document in documents]
    )

def main():
    documents = load_dataset(ChromaConfig().DATASET_PATH)
    save_data_to_vector_db(
        client=ChromaConfig().get_client(),
        collection_name=ChromaConfig().COLLECTION_NAME,
        embedding_function=ChromaConfig().get_embedding_function(),
        documents=documents
    )

if __name__ == '__main__':
    main()