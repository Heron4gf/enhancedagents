
import os
from dotenv import load_dotenv

load_dotenv()

LITELLM_HEADERS = {
    "Helicone-Auth": f"Bearer {os.getenv('HELICONE_API_KEY')}",
    "Helicone-Target-Url": "https://openrouter.ai",
    "Helicone-Target-Provider": "OpenRouter",
    "Helicone-Cache-Enabled": "true",
    "Cache-Control": "max-age=3600",
    "Helicone-LLM-Security-Enabled": "true"
}

APP_CONFIG = {
    "APP_NAME": "my_first_adk_app",
    "USER_ID": "user_test_1",
    "SESSION_ID": "session_abc_123",
    "MODEL": "meta-llama/llama-4-scout:free",
    "API_BASE": "https://gateway.helicone.ai/api/v1"
}
