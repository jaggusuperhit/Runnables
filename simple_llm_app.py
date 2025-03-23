import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# OpenRouter API details
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "gpt-3.5-turbo"  # Specify the model

# Define the topic input
topic = input("Enter a topic: ")
formatted_prompt = f"Suggest a catchy blog title about {topic}."

# Prepare the payload
payload = {
    "model": MODEL_NAME,
    "messages": [{"role": "user", "content": formatted_prompt}],
    "temperature": 0.7,
}

# Set up headers with your API key
headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
}

# Make the API request
response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers)

# Handle the response
if response.status_code == 200:
    blog_title = response.json()["choices"][0]["message"]["content"]
    print("Generated Blog Title:", blog_title)
else:
    print("Error:", response.status_code, response.text)
