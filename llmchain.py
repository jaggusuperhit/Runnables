import requests
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# OpenRouter API details
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # Fetch API key from .env
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Function to call OpenRouter API
def call_openrouter_api(prompt: str) -> str:
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

# Create a Prompt Template
prompt = PromptTemplate(
    input_variables=['topic'],  # Defines what input is needed
    template="Suggest a catchy blog title about {topic}."
)

# Define the LLM as a callable function
def openrouter_llm(input_text: str) -> str:
    return call_openrouter_api(input_text)

# Create a RunnableSequence
chain = (
    {"topic": RunnablePassthrough()}  # Pass the input directly
    | prompt  # Format the prompt
    | (lambda x: x.text)  # Extract the string value from the PromptValue
    | openrouter_llm  # Call the LLM
)

# Run the chain with a specific topic
topic = input('Enter the topic: ')
output = chain.invoke(topic)

print("Generated Blog Title:", output)