from chroma_config import ChromaConfig
from chromadb import ClientAPI

def retrieve_documents(client: ClientAPI, collection_name, embedding_function, query, n=2):
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_function
    )
    results = collection.query(
        query_texts=[query],
        n_results=n
    )
    return results

def generate_output():
    pass

def main():
    query = 'Quais são as formas de pagamento?'
    documents = retrieve_documents(
        client=ChromaConfig().get_client(),
        collection_name=ChromaConfig().COLLECTION_NAME,
        embedding_function=ChromaConfig().get_embedding_function(),
        query=query
    )
    print(documents)

if __name__ == '__main__':
    main()