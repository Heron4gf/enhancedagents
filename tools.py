
import os
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.langchain_tool import LangchainTool
from langchain_community.tools import TavilySearchResults

def remember_something(data_to_remember: str, tool_context: ToolContext) -> dict:
    """Reads previous data from state and saves new data."""
    previous_data = tool_context.state.get("user_data", "nothing")
    tool_context.state["user_data"] = data_to_remember
    return {
        "status": "success", 
        "message": f"I remembered '{data_to_remember}'. Before that, I knew about '{previous_data}'."
    }

def read_file(path: str) -> str:
    with open(path, 'r') as f:
        return f.read()

def overwrite_file(path: str, content: str):
    with open(path, 'w') as f:
        f.write(content)

def run_command(command: str):
    os.system(command)

def get_tools():
    tavily_search_tool = TavilySearchResults(
        max_results=3,
        include_answer=True
    )
    adk_tavily_tool = LangchainTool(tool=tavily_search_tool)
    
    return [read_file, run_command, overwrite_file, adk_tavily_tool, remember_something]
