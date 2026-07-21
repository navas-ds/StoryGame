# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from .prompt import SYSTEM_PROMPT
from dotenv import load_dotenv

load_dotenv()

def generate_answer(query: str, docs: list):
    """
    Combines text chunks into a context block, sends it to the Gemini LLM,
    and returns a clean payload containing the text answer and clear citations.
    """
    # Initialize the LLM tool dynamically using setup configurations
    llm = ChatGroq(
        model="qwen/qwen3-32b",
        temperature=0  # Zero temperature forces deterministic, factual answers
    )

    # Merge all chunk text contents together separated by clear breaks
    context_text = "\n\n".join(doc.page_content for doc in docs)

    # Build the linear chain prompt template matching LangChain specifications
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "Context:\n{context}\n\nQuestion:\n{question}")
    ])

    # Connect the pieces together into a simple execution pipeline
    execution_chain = prompt_template | llm

    # Execute the LLM pipeline
    response = execution_chain.invoke({
        "context": context_text,
        "question": query
    })

    # Build the citations list tracking back to source files
    source_citations = []
    for doc in docs:
        metadata = doc.metadata
        source_citations.append({
            "document": metadata.get("source_file", "Unknown Document"),
            "page": metadata.get("page", 1)
        })

    # Return a clean structural dictionary containing the output
    return {
        "answer": response.content,
        "citations": source_citations
    }
