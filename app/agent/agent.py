# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from .tools import TOOLS
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq model connection engine
llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0
)

# Fixed: MessagesPlaceholder structured accurately to support internal langsmith/agent trace logs
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a multi-step Smart Document Assistant agent with access to local tools.

Operational Directives:
1. Break user requests down into sequential logical extraction tasks.
2. If document data is requested, activate 'document_search'.
3. If calculation logic or statistical checks are required over extracted facts, pass them to 'calculator'.
4. If checking times or relative statements, invoke 'datetime_tool'.
5. Answer questions completely and factually. Ground all claims using source documents when available."""
    ),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# Initialize tool calling architecture
agent = create_tool_calling_agent(llm, TOOLS, prompt)

def get_agent_executor():
    """
    Functional generation accessor to spawn a safe, un-blocked 
    traceable agent routing executor instance dynamically.
    """
    return AgentExecutor(
        agent=agent,
        tools=TOOLS,
        verbose=True,
        return_intermediate_steps=True  # Provides multi-step analytical log streams for evaluation parameters
    )
