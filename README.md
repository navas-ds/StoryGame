# Smart Document Assistant

An advanced, enterprise-ready **Smart Document Assistant** combining a highly factual Retrieval-Augmented Generation (RAG) data pipeline with a multi-step ReAct Agent. Built entirely using modern **procedural functional programming standard** (completely free of object-oriented class overhead), this system uses a stateless FastAPI backend and an interactive Streamlit frontend. 

It satisfies all standard and bonus deliverables—including multi-step tool routing, mathematical equation evaluation security, persistent conversation multi-session isolation, and expandable reasoning thought-trace logs.

---

### 🏗️ System Architecture

```text
┌────────────────────────────────────────────────────────┐
│               Streamlit User Interface (UI)            │
└───────────────────────────┬────────────────────────────┘
                            │ Sends user message + Session ID
                            ▼
┌────────────────────────────────────────────────────────┐
│                 FastAPI Backend Server                 │
└───────────────────────────┬────────────────────────────┘
                            │
         ┌──────────────────┴──────────────────┐
         ▼                                     ▼
┌──────────────────────────────┐     ┌──────────────────────────────┐
│     AI Agent Controller      │     │    Document RAG Pipeline     │
│   (Manages Conversation)     │     │   (Reads & Stores Files)     │
└────────┬──────────────┬──────┘     └──────────────┬───────────────┘
         │              │                           │
         │ Runs Math    │ Checks Time               │ Searches Text
         ▼              ▼                           ▼
┌────────────────┐┌──────────────┐   ┌──────────────────────────────┐
│  Calculator    ││  Clock Tool  │   │     Chroma Vector Database   │
│ (Secure Math)  ││ (System Time)│   │    (Stores Text Fragments)   │
└────────────────┘└──────────────┘   └──────────────────────────────┘
```



### 🧬 Core Components Split
1. **The Ingestion Pipeline (`app/rag/`)**: Reads and maps structural document text blocks (`PyPDFLoader`, `TextLoader`) into vector segments using local `sentence-transformers/all-MiniLM-L6-v2` embeddings, storing outputs inside a local persistent `ChromaDB` layer.
2. **The Modern Agent Loop (`app/agent/`)**: Powered by the modern standard **LangGraph React Agent** (`create_react_agent`), bypassing obsolete legacy executors. It parses user intents to route operations dynamically across tools.
3. **The Session Memory Vault (`app/memory/`)**: Isolates multi-user context states natively via an automatic checkpointer matching individual unique `session_id` UUID tokens to prevent context bleeding across different tabs.

---

## 🛠️ Secure Multi-Step Tools Capability

The agent automatically coordinates complex operations by executing and chaining three built-in standalone tools:
* **`document_search`**: Automatically queries the persistent vector database using a custom top-k similarity calculation. If the retrieved context cannot satisfy a request, strict system prompt constraints force the fallback string: *"I don't know based on the provided documents."*
* **`calculator`**: Safely evaluates mathematical equations using Python's **Abstract Syntax Tree (`ast`) parser** instead of a raw `eval()` block, blocking system command injection vulnerabilities.
* **`datetime_tool`**: Provides direct visibility into the operational host system clock to track temporal and baseline calendar statements.

---

## 🚀 Local Installation & Execution Checklist

Follow these steps sequentially to setup and launch the application ecosystem locally on your development environment without containers:

### 1. Environment Configurations
Clone your repository, establish a dedicated Python virtual environment, and activate it:

git clone https://github.com/navas-ds/StoryGame.git

create venv
### 2. Install Project Dependencies
Install all structural core packages using `pip`:

pip install -r requirements.txt


### 3. set groq API_KEY on the .env variable


### 4. Start the Application Stack
Open two terminal windows side by side to launch the independent services:

* **Terminal A (FastAPI Backend Server)**:
  ```bash
  python main.py
  ```
  *The API will boot up and bind to network port `http://localhost:8000`. You can inspect the fully interactive visual API testing workbench natively via `http://localhost:8000/docs`.*

* **Terminal B (Streamlit Dashboard UI)**:
  ```bash
  streamlit run ui/streamlit.py
  ```
  *The user interface workspace will automatically launch a tab inside your default browser routing to `http://localhost:8501`.*

---



## 🗂️ Project Repository Tree

```text
smart_assistant/
│
├── app/
│   ├── api/
│   │   └── routes.py         # Versioned endpoints (/chat, /documents, /history)
│   ├── agent/
│   │   ├── agent.py          # LangGraph create_react_agent orchestrator orchestration
│   │   ├── tools.py          # Unified tool schema registry layer
│   │   ├── calculator.py     # Safe Abstract Syntax Tree (AST) math engine
│   │   ├── datetime_tool.py  # System execution clock interface tool
│   │   └── search_tool.py    # Standardized retrieval bridging adapter
│   ├── memory/
│   │   └── memory.py         # Functional state array tracking hooks
│   ├── rag/
│   │   ├── chunking.py       # Recursive text subdivision logic 
│   │   ├── embedding.py      # HuggingFace vector embedding allocator
│   │   ├── loader.py         # Standardized metadata extraction loader
│   │   └── vectorstore.py    # Persistent ChromaDB integration layer
│   └── main.py               # FastAPI application bootstrapping file
│
├── ui/
│   └── streamlit_app.py      # Streamlit chat interface and thought tracer
│
├── documents/                # Local cache folder for file uploads
├── chroma_db/                # Persistent vector database directory
└── requirements.txt          # Global application dependency manifest
```
