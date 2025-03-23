import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# OpenRouter API details
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Check if the document file exists
file_path = "D:/Gen AI Langchain/Chains/Runnables/docs.txt"  # Absolute path
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

# Load document content
with open(file_path, "r", encoding="utf-8") as file:
    document_content = file.read()

# Function to interact with OpenRouter API
def call_openrouter_api(prompt: str) -> str:
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
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
        raise Exception(f"API Error: {response.status_code}, {response.text}")

# Query and API call
query = "What are the key takeaways from the document?"
prompt = f"Based on the following text, answer the question: {query}\n\n{document_content}"
response = call_openrouter_api(prompt)

# Output the result
print("Answer:", response)
