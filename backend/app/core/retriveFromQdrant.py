from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os

load_dotenv()

async def retriveErrorData(query, k=5):
    # Check if query is empty or None
    if not query or not query.strip():
        print("Warning: Empty query provided to retriveErrorData")
        return "No specific error guidance available. Please check for common Manim v0.19 syntax issues."
    
    embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key= os.getenv("GOOGLE_API_KEY")
    )

    retriver = QdrantVectorStore.from_existing_collection(
        collection_name="mainmVideo",
        embedding=embeddings,
        url="https://f83a9a46-c78e-4f8f-ae92-e9c958787fbe.eu-west-2-0.aws.cloud.qdrant.io:6333",
        api_key=os.getenv("QDRANT_API_KEY"),
        # url="http://localhost:6333"
    )

    try:
        relevant_chunk = retriver.similarity_search(
            query=query,
            k=10
        )

        if relevant_chunk and len(relevant_chunk) > 0:
            print("\n\n qdrant db: ",relevant_chunk[0].page_content)
            return relevant_chunk[0].page_content
        else:
            return "No relevant error guidance found in the database."
    except Exception as e:
        print(f"Error retrieving data from Qdrant: {e}")
        return "Error retrieving guidance data. Please check for common Manim v0.19 syntax issues."