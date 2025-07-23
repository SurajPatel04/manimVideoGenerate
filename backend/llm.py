from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os


load_dotenv()

safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}


llmFlash = ChatGoogleGenerativeAI(
    api_key = os.getenv("GOOGLE_API_KEY"),
    model="gemini-2.5-flash",
)

llmPro = ChatGoogleGenerativeAI(
    api_key = os.getenv("GOOGLE_API_KEY"),
    model="gemini-2.5-pro",
    safety_settings=safety_settings
)

llmFlashLite = ChatGoogleGenerativeAI(
    api_key = os.getenv("GOOGLE_API_KEY"),
    model = "gemini-2.0.flash-lite"
)