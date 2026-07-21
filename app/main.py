import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router

def create_app() -> FastAPI:
    """
    Initializes and configures the FastAPI application instance.
    Keeps everything procedural and modular.
    """
    # Initialize the main FastAPI backend app
    app = FastAPI(
    )

    # Configure CORS middleware so your Streamlit UI can talk to it seamlessly
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins for local prototype testing
        allow_credentials=True,
        allow_methods=["*"],  # Allows standard GET, POST, OPTIONS, etc.
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/api/v1")
    return app

# Generate the app instance that Uvicorn or Docker will point to
app = create_app()

# Allows direct script execution for fast local debugging
if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        port=8000, 
        reload=True
    )
