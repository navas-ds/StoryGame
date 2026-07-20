# Fixed: Importing the optimized functional RAG retriever pipeline step
from app.rag.retriever import retrieve_documents

def search_documents(query: str):
    """Executes search matches against the vector storage database."""
    docs = retrieve_documents(query)
    
    # Format the document blocks into clean readable strings for the Agent loop
    formatted_context = []
    for doc in docs:
        filename = doc.metadata.get("source_file", "Unknown File")
        page = doc.metadata.get("page", 1)
        formatted_context.append(f"[Source: {filename}, Page: {page}]\nContent: {doc.page_content}")
        
    return "\n\n---\n\n".join(formatted_context)
