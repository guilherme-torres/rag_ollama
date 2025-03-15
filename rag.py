from chroma_config import ChromaConfig
from chromadb import ClientAPI
import ollama

def retrieve_documents(client: ClientAPI, collection_name, embedding_function, query, n=3):
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_function
    )
    results = collection.query(
        query_texts=[query],
        n_results=n
    )
    return results

def generate_output(query: str, documents: list):
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
        model=ChromaConfig().MODEL_NAME,
        prompt=prompt,
        options={
            'temperature': 0
        }
    )
    return output.response

def main():
    query = 'Como faço para entrar em contato?'
    result = retrieve_documents(
        client=ChromaConfig().get_client(),
        collection_name=ChromaConfig().COLLECTION_NAME,
        embedding_function=ChromaConfig().get_embedding_function(),
        query=query
    )
    documents = result['documents'][0]
    output = generate_output(query=query, documents=documents)
    print(output)

if __name__ == '__main__':
    main()