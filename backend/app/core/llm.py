from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env')
load_dotenv(dotenv_path=env_path)

def get_google_llm_lite():
    return init_chat_model(
        "gemini-2.5-flash-lite",
        model_provider="google_vertexai",
        temperature=0,
        streaming=True
    )

def get_google_llm():
    return init_chat_model(
        "gemini-2.5-flash",
        model_provider="google_vertexai",
        temperature=0,
        streaming=True,
    )

llmFlash = get_google_llm()
llmFlashLite = get_google_llm_lite()

llmPro = init_chat_model(
    "gemini-2.5-pro",
    model_provider="google_vertexai",
    temperature=0,
    streaming=True,
)

def get_openai_llm():
    return init_chat_model(
        "gpt-4o-mini",
        model_provider="openai",
        temperature=0,
        streaming=True,
        api_key=os.environ.get("OPENAI_API_KEY")
    )

llmOpenAI = get_openai_llm()
