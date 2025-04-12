from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import litellm
import os
from dotenv import load_dotenv
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

from google.adk.tools.tool_context import ToolContext
from google.adk.tools.langchain_tool import LangchainTool
from langchain_community.tools import TavilySearchResults

def remember_something(data_to_remember: str, tool_context: ToolContext) -> dict:
    """Reads previous data from state and saves new data."""
    print("--- Tool: remember_something called ---")

    # Read from state (use .get() for safety)
    previous_data = tool_context.state.get("user_data", "nothing")
    print(f"--- Tool: Found previous data: '{previous_data}' ---") #

    # Write new data to state
    tool_context.state["user_data"] = data_to_remember # [cite: 354]
    print(f"--- Tool: Saved new data: '{data_to_remember}' ---")

    return {"status": "success", "message": f"I remembered '{data_to_remember}'. Before that, I knew about '{previous_data}'."}

load_dotenv()

litellm.headers = {
            "Helicone-Auth": f"Bearer {os.getenv('HELICONE_API_KEY')}",
            "Helicone-Target-Url": "https://openrouter.ai",
            "Helicone-Target-Provider": "OpenRouter",
            "Helicone-Cache-Enabled": "true",
            "Cache-Control": "max-age=3600",
            "Helicone-LLM-Security-Enabled": "true"
        }

APP_NAME = "my_first_adk_app"
USER_ID = "user_test_1" # Identifier for the user
SESSION_ID = "session_abc_123" # Identifier for this specific conversation

# 1. Create the Session Service instance
session_service = InMemorySessionService()

session = session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID
    # state={"initial_key": "initial_value"} # Optional: initial state
)

def read_file(path: str) -> str:
    with open(path, 'r') as f:
        return f.read()


def overwrite_file(path: str, content: str):
    with open(path, 'w') as f:
        f.write(content)

def run_command(command: str):
    os.system(command)

tavily_search_tool_instance = TavilySearchResults(
    max_results=3,
    include_answer=True # Ask Tavily to provide a direct answer if possible
)

# Wrap it with ADK's LangchainTool
adk_tavily_tool = LangchainTool(tool=tavily_search_tool_instance)

main_agent = Agent(
    name="main_agent",
    model=LiteLlm(
        model="meta-llama/llama-4-scout:free",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        api_base="https://gateway.helicone.ai/api/v1"
    ),
    instruction="You're a great pc agent, with access to a windows computer and with need to help a user",
    description="",
    tools=[read_file, run_command, overwrite_file, adk_tavily_tool, remember_something]
)

runner = Runner(
    agent=main_agent, # Your agent defined earlier
    app_name=APP_NAME,
    session_service=session_service
)