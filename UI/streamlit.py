import streamlit as st
import requests
import uuid

# Base API endpoint
API_URL = "http://localhost:8000/api/v1"

# 1. Page Configuration Setup (Executed immediately on load)
st.set_page_config(
    page_title="Smart Document Assistant",
    layout="wide"
)

# 2. Session State Initialization
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())  # Creates a permanent session tracking string

if "messages" not in st.session_state:
    st.session_state.messages = []  # Local UI memory cache state array

# 3. Sidebar UI: Document File Management
with st.sidebar:
    st.title("📂 Document Center")

    # Place this functional action button inside the sidebar block of streamlit_app.py
    if st.button("➕ Start New Chat Session", use_container_width=True, help="Switches to a fresh chat session without deleting old ones."):
        # Step A: Generate a brand new unique session token
        st.session_state.session_id = str(uuid.uuid4())
        
        # Step B: Clear only the local frontend UI screen message display array
        st.session_state.messages = []
        
        # Step C: Show a quick visual success alert
        st.toast("Switched to a brand new chat session!", icon="🚀")
        
        # Step D: Force Streamlit to instantly re-render the pristine empty workspace layout
        st.rerun()

    st.divider()
    st.write("Upload knowledge manuals or reference guides to query your assistant.")
    
    # File Uploader Widget
    uploaded_file = st.file_uploader(
        "Choose a file", 
        type=["pdf", "txt", "md"], 
        help="Supported file types: .pdf, .txt, .md"
    )
    
    if uploaded_file is not None:
        if st.button("📤 Process & Index Document", use_container_width=True):
            with st.spinner("Processing ingestion pipeline..."):
                try:
                    # Prepare file payload matching FastAPI requirements
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    response = requests.post(f"{API_URL}/documents/upload", files=files)
                    
                    if response.status_code == 200:
                        st.success(f"Successfully processed: {uploaded_file.name}")
                    else:
                        st.error(f"Upload failed: {response.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Could not connect to backend server: {str(e)}")
                    
    st.divider()
    
    # Active Files Display Panel
    st.subheader("📚 Loaded System Repositories")
    try:
        doc_list_resp = requests.get(f"{API_URL}/documents")
        if doc_list_resp.status_code == 200:
            available_files = doc_list_resp.json()
            if available_files:
                for file_name in available_files:
                    st.caption(f"📄 {file_name}")
            else:
                st.info("No documents uploaded yet.")
        else:
            st.warning("Failed to fetch document inventory registry.")
    except Exception:
        st.caption("⚠️ Backend unavailable to populate document tracking view.")

# 4. Main Core UI: Interaction Workspace Layout
st.title(" Smart Document Assistant")
st.write("Ask questions")

# Render Historical Local Conversation Trail Elements
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        # Check if reasoning steps exist for historical traces
        if msg.get("reasoning") and msg["role"] == "assistant":
            with st.expander("🔍 Review Agent Analytical Reasoning Log"):
                for step in msg["reasoning"]:
                    st.markdown(f"**Activated Tool:** `{step.get('tool_activated')}`")
                    st.markdown(f"**Arguments Sent:** `{step.get('tool_input')}`")
                    st.markdown(f"**Execution Output:** {step.get('tool_output_received')}")
                    st.divider()

# 5. Core Operational Input Loop Routine
if user_prompt := st.chat_input("Enter your question or analytical prompt here..."):
    
    # Immediately render user statement locally
    with st.chat_message("user"):
        st.write(user_prompt)
        
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    # Trigger API network connection pipeline
    with st.chat_message("assistant"):
        with st.spinner("Agent parsing multi-step strategy..."):
            try:
                chat_payload = {
                    "session_id": st.session_state.session_id,
                    "message": user_prompt
                }
                
                response = requests.post(f"{API_URL}/chat", json=chat_payload)
                
                if response.status_code == 200:
                    data = response.json()
                    answer_text = data.get("answer", "")
                    reasoning_steps = data.get("reasoning", [])
                    
                    # Print final assistant statement downstream
                    st.write(answer_text)
                    
                    # If the agent engaged custom tools, render out the intermediate chain execution trace logs
                    if reasoning_steps:
                        with st.expander("🔍 Review Agent Analytical Reasoning Log", expanded=False):
                            for step in reasoning_steps:
                                st.markdown(f"**Activated Tool:** `{step.get('tool_activated')}`")
                                st.markdown(f"**Arguments Sent:** `{step.get('tool_input')}`")
                                st.markdown(f"**Execution Output:** {step.get('tool_output_received')}")
                                st.divider()
                                
                    # Commit payload block context state directly to memory cache structures
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer_text,
                        "reasoning": reasoning_steps
                    })
                    
                else:
                    error_msg = response.json().get('detail', 'Internal server operational fault.')
                    st.error(f"Error calling agent engine: {error_msg}")
                    
            except Exception as e:
                st.error(f"Failed to communicate with agent service: {str(e)}")


