import requests
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings  # Still using OpenAI embeddings for simplicity
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# OpenRouter API details
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # Fetch API key from .env
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Load the document
loader = TextLoader("docs.txt")  # Ensure docs.txt exists
documents = loader.load()

# Split the text into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

# Convert text into embeddings & store in FAISS
vectorstore = FAISS.from_documents(docs, OpenAIEmbeddings())  # Still using OpenAI embeddings

# Create a Retriever (fetches relevant documents)
retriever = vectorstore.as_retriever()

# Manually Retrieve Relevant Documents
query = "What are the key takeaways from the document?"
retrieved_docs = retriever.get_relevant_documents(query)

# Combine Retrieved Text into a Single Prompt
retrieved_text = "\n".join([doc.page_content for doc in retrieved_docs])

# Function to call OpenRouter API
def call_openrouter_api(prompt):
    payload = {
        "model": "gpt-3.5-turbo",  # Specify the model
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,  # Adjust temperature as needed
    }
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

# Manually Pass Retrieved Text to OpenRouter API
prompt = f"Based on the following text, answer the question: {query}\n\n{retrieved_text}"
answer = call_openrouter_api(prompt)

# Print the Answer
print("Answer:", answer)