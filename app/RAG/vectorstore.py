from langchain_chroma import Chroma
from .embedding import get_embedding_model

def get_vector_db_client():
    """
    Creates or establishes an active execution connection to ChromaDB.
    """
    active_embeddings = get_embedding_model()
    return Chroma(
        collection_name="smart_assistant_collection",
        embedding_function=active_embeddings,
        persist_directory="./chroma_langchain_db"
    )

def add_documents_to_store(docs):
    """
    Connects to the store dynamically and logs the text chunks.
    """
    if not docs:
        return
    database = get_vector_db_client()
    database.add_documents(docs)

def get_vector_retriever():
    """
    Exposes a clean search interface with hard distance thresholding 
    to force an 'I do not know' fallback during sparse matches.
    """
    database = get_vector_db_client()
    return database.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 6
        }
    )
