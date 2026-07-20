import torch
from langchain_huggingface import HuggingFaceEmbeddings

EMBEDDING_MODEL="all-MiniLM-L6-v2"
def get_embedding_model():
    """
    Handles local hardware orchestration natively. 
    Prevents thread lockups when calculating embedding layers.
    """
    if torch.cuda.is_available():
        target_device = "cuda"
    elif torch.backends.mps.is_available():
        target_device = "mps"
    else:
        target_device = "cpu"

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": target_device},
        encode_kwargs={"normalize_embeddings": True}
    )
