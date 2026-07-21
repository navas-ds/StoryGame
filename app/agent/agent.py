# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from .tools import TOOLS
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq model connection engine
llm = ChatGroq(
    model="qwen/qwen3.6-27b",
    temperature=0
)

SYSTEM_PROMPT = """You are a multi-step Smart Document Assistant agent with access to local tools.

Operational Directives:
1. Break user requests down into sequential logical extraction tasks.
2. If document data is requested, activate 'document_search'.
3. If calculation logic or statistical checks are required over extracted facts, pass them to 'calculator'.
4. If checking times or relative statements, invoke 'datetime_tool'.
5. Answer questions completely and factually. Ground all claims using source documents when available."""


# Initialize tool calling architecture
agent_runtime = create_agent(
    model=llm,
    tools=TOOLS,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=InMemorySaver())

def get_agent_executor():
    """
    Functional generation accessor to spawn a safe, un-blocked 
    traceable agent routing executor instance dynamically.
    """
    return agent_runtime
