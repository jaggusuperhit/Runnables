import requests
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Debugging: Print current directory and check if file exists
current_directory = os.getcwd()
print("Current Directory:", current_directory)
file_path = "D:/Gen AI Langchain/Chains/Runnables/docs.txt"  # Absolute path
print("File Path:", file_path)
print("File Exists:", os.path.exists(file_path))

# OpenRouter API details
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # Fetch API key from .env
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

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

# Load the document
loader = TextLoader(file_path)  # Use absolute path
documents = loader.load()

# Split the text into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

# Convert text into embeddings & store in FAISS
vectorstore = FAISS.from_documents(docs, OpenAIEmbeddings())

# Create a retriever (this fetches relevant documents)
retriever = vectorstore.as_retriever()

# Define the LLM as a callable function
def openrouter_llm(prompt: str) -> str:
    return call_openrouter_api(prompt)

# Create RetrievalQAChain
qa_chain = RetrievalQA.from_chain_type(
    llm=openrouter_llm,  # Use the OpenRouter LLM
    retriever=retriever
)

# Ask a question
query = "What are the key takeaways from the document?"
answer = qa_chain.run(query)

print("Answer:", answer)