from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os


load_dotenv()


llmFlash = ChatGoogleGenerativeAI(
    # api_key = os.getenv("GOOGLE_API_KEY"),
    model="gemini-2.5-flash",
)

llmPro = ChatGoogleGenerativeAI(
    # api_key = os.getenv("GOOGLE_API_KEY"),
    model="gemini-2.5-pro",
)

llmFlashLite = ChatGoogleGenerativeAI(
    # api_key = os.getenv("GOOGLE_API_KEY"),
    model = "gemini-2.0.flash-lite"
)