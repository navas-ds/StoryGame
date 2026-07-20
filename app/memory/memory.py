from langchain_core.chat_history import InMemoryChatMessageHistory

# Global execution dictionary mapping session strings to active chat state vectors
history_store = {}

def get_session_history(session_id: str):
    if session_id not in history_store:
        # Upgraded to modern core class to ensure full alignment with AgentExecutor workflows
        history_store[session_id] = InMemoryChatMessageHistory()
        
    return history_store[session_id]

def clear_session_history(session_id: str) -> bool:
    """
    Safely purges memory data vectors for a specific user session 
    to free up application server RAM.
    """
    if session_id in history_store:
        del history_store[session_id]
        return True
    return False
