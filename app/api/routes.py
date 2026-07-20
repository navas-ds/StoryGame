import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

# Safe, lowercase imports to guarantee seamless compilation under Linux Docker containers
from app.rag.loader import load_document
from app.rag.chunking import split_documents
from app.rag.vectorstore import add_documents_to_store

from app.agent.agent import get_agent_executor
from app.memory.memory import get_session_history

router = APIRouter()

UPLOAD_FOLDER = "documents"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Pydantic schema enforcing incoming JSON shape validation
class ChatRequest(BaseModel):
    session_id: str
    message: str


@router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    """Asynchronously streams incoming file attachments to storage and registers them to ChromaDB."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="Uploaded file lacks a valid name structure.")
        
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    
    try:
        # Write binary stream down cleanly
        with open(path, "wb") as buffer:
            # Note: For production large payloads, async chunk reading is ideal, 
            # but file.file works safely here.
            buffer.write(file.file.read())

        # Procedural execution pipeline chain
        docs = load_document(path)
        chunks = split_documents(docs)
        add_documents_to_store(chunks)

        return {
            "filename": file.filename,
            "status": "uploaded"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File processing pipeline failed: {str(e)}")


@router.get("/documents")
def list_documents():
    """Lists every raw knowledge source file currently present inside the local repository upload cache."""
    if not os.path.exists(UPLOAD_FOLDER):
        return []
    return os.listdir(UPLOAD_FOLDER)


@router.post("/chat")
def chat(request: ChatRequest):
    """Processes message requests through a multi-step agent tracking historical sessions."""
    # Fetch active session storage interface
    history = get_session_history(request.session_id)
    
    # Extract existing conversation history logs BEFORE appending the new message
    # This prevents the agent from seeing the new prompt duplicated inside the context log
    past_messages = history.messages.copy()

    # Append current user prompt message context to historical storage
    history.add_user_message(request.message)

    # Spawn fresh agent routing execution instance
    executor = get_agent_executor()
    
    try:
        # Execute query passing BOTH current input text string AND historical memory sequences
        result = executor.invoke({
            "input": request.message,
            "chat_history": past_messages
        })

        output_text = result.get("output", "")
        
        # Save AI output context back to session history securely
        history.add_ai_message(output_text)

        # FIXED: Serialize complex multi-step intermediate structures to basic strings to prevent FastAPI crashes
        raw_steps = result.get("intermediate_steps", [])
        clean_reasoning_steps = []
        
        for action, observation in raw_steps:
            clean_reasoning_steps.append({
                "tool_activated": getattr(action, "tool", "Unknown Tool"),
                "tool_input": getattr(action, "tool_input", ""),
                "thought_log": getattr(action, "log", ""),
                "tool_output_received": str(observation)
            })

        return {
            "answer": output_text,
            "reasoning": clean_reasoning_steps
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent execution timeout or error: {str(e)}")


@router.get("/chat/{session_id}/history")
def get_chat_history(session_id: str):
    """Retrieves standard history structures mapped directly to the active session index string."""
    chat_history = get_session_history(session_id)
    return [
        {
            "type": msg.type,
            "content": msg.content
        }
        for msg in chat_history.messages
    ]
