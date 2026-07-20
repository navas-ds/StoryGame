from .vectorstore import get_vector_retriever

def retrieve_documents(query: str):
    retriever = get_vector_retriever()
    
    # Invoke it directly with the user's text query
    return retriever.invoke(query)
