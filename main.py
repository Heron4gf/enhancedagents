from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import litellm
import os
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

from config import LITELLM_HEADERS, APP_CONFIG
from tools import get_tools

def main():
    # Configure LiteLLM
    litellm.headers = LITELLM_HEADERS

    # Create session service
    session_service = InMemorySessionService()
    session = session_service.create_session(
        app_name=APP_CONFIG["APP_NAME"],
        user_id=APP_CONFIG["USER_ID"],
        session_id=APP_CONFIG["SESSION_ID"]
    )

    # Create main agent
    main_agent = Agent(
        name="main_agent",
        model=LiteLlm(
            model=APP_CONFIG["MODEL"],
            api_key=os.getenv("OPENROUTER_API_KEY"),
            api_base=APP_CONFIG["API_BASE"]
        ),
        instruction="You're a great pc agent, with access to a windows computer and with need to help a user",
        description="A versatile PC assistant with file and system access capabilities",
        tools=get_tools()
    )

    # Create and return runner
    runner = Runner(
        agent=main_agent,
        app_name=APP_CONFIG["APP_NAME"],
        session_service=session_service
    )

    return runner

if __name__ == "__main__":
    runner = main()