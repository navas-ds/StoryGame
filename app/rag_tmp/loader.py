from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader

def load_document(file_path: str):
    """
    Loads documents safely by type and returns a copy of documents 
    with completely standardized citation metadata keys.
    """
    path_obj = Path(file_path)
    
    if not path_obj.exists():
        raise FileNotFoundError(f"Target document not found at: {file_path}")
        
    suffix = path_obj.suffix.lower()

    # Route based on explicit file types
    if suffix == ".pdf":
        loader = PyPDFLoader(file_path=str(file_path))
    elif suffix in [".txt", ".md"]:
        loader = TextLoader(file_path=str(file_path), encoding="utf-8")
    else:
        raise ValueError(f"Unsupported format '{suffix}'. Please use PDF, TXT, or MD.")

    loaded_docs = loader.load()
    standardized_docs = []
    
    # Immutable metadata modification loop
    for doc in loaded_docs:
        # Create a clean, independent copy of the metadata dictionary
        clean_metadata = dict(doc.metadata)
        clean_metadata["source_file"] = path_obj.name
        
        # Ensure 'page' reference always maps to an integer for citation logic
        if "page" not in clean_metadata:
            clean_metadata["page"] = 1
            
        doc.metadata = clean_metadata
        standardized_docs.append(doc)
                
    return standardized_docs
