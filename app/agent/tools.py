from langchain.tools import tool
from .calculator import calculate
from .datetime_tool import current_datetime
from .search_tool import search_documents

# Pass the tool name as a direct string, and override description as a keyword argument
@tool("calculator", description="Performs arithmetic calculations. Use this for any math equations, sums, or percentages.")
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression string safely."""
    return str(calculate(expression))


@tool("datetime_tool", description="Returns the current system date and time. Use this when answering questions about deadlines or temporal statements.")
def datetime_tool() -> str:
    """Return current date and time."""
    return current_datetime()


@tool("document_search", description="Queries the uploaded document vector store database. Pass optimized keyword strings as the input query.")
def document_search(query: str) -> str:
    """Search uploaded documents and return matching text blocks."""
    return search_documents(query)


# Consolidated global tool registry array vector
TOOLS = [
    calculator,
    datetime_tool,
    document_search,
]
