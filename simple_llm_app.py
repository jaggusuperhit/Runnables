import requests
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv  # Import the load_dotenv function
import os  # Import os to access environment variables

# Load environment variables from .env file
load_dotenv()

# OpenRouter API details
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # Fetch API key from .env
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Specify the model you want to use
MODEL_NAME = "gpt-3.5-turbo"  # Explicitly using GPT-3.5 Turbo

# Create a Prompt Template
prompt = PromptTemplate(
    input_variables=['topic'],
    template="Suggest a catchy blog title about {topic}."
)

# Define the input
topic = input('Enter a topic: ')

# Format the prompt using PromptTemplate
formatted_prompt = prompt.format(topic=topic)

# Prepare the payload for the OpenRouter API
payload = {
    "model": MODEL_NAME,  # Using GPT-3.5 Turbo
    "messages": [
        {"role": "user", "content": formatted_prompt}
    ],
    "temperature": 0.7,  # Adjust temperature as needed
}

# Set up headers with your API key
headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
}

# Make the API request to OpenRouter
response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Extract the generated blog title from the response
    blog_title = response.json()["choices"][0]["message"]["content"]
    print("Generated Blog Title:", blog_title)
else:
    print("Error:", response.status_code, response.text)