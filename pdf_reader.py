import requests
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Print to confirm script execution
print("Starting pdf_reader script...")

# Load environment variables from .env file
load_dotenv()
print("Environment variables loaded.")

# OpenRouter API details
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # Fetch API key from .env
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Check if docs.txt exists
if not os.path.exists("docs.txt"):
    logging.error("docs.txt file not found.")
    raise FileNotFoundError("docs.txt file not found.")

# Load the document
loader = TextLoader("docs.txt")
documents = loader.load()
print("Documents loaded successfully.")

# Split the text into smaller chunks
chunk_size = int(os.getenv("CHUNK_SIZE", 500))  # Default chunk size
chunk_overlap = int(os.getenv("CHUNK_OVERLAP", 50))  # Default chunk overlap
text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
docs = text_splitter.split_documents(documents)
print(f"Documents split into {len(docs)} chunks.")

# Custom function to call OpenRouter API
def call_openrouter_api(prompt: str) -> str:
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
    }
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        logging.error(f"API call failed with status code {response.status_code}: {response.text}")
        raise Exception(f"Error: {response.status_code}, {response.text}")

# Query for relevant information
query = "What are the key takeaways from the document?"
logging.info("Querying for relevant documents: %s", query)

# Simulate document retrieval (replace with your own logic)
retrieved_text = "\n".join([doc.page_content for doc in docs])  # Combine chunks for simplicity

# Manually pass retrieved text to OpenRouter API
prompt = f"Based on the following text, answer the question: {query}\n\n{retrieved_text}"
answer = call_openrouter_api(prompt)

# Log and print the response
logging.info("Retrieved Answer: %s", answer)
print("Answer from OpenRouter:", answer)

print("Script execution completed.")
