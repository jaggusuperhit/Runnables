import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# OpenRouter API details
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # Fetch API key from .env
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Specify the model you want to use
MODEL_NAME = "gpt-3.5-turbo"  # You can change this to any model supported by OpenRouter

# Function to get input JSON schema for the model
def get_input_jsonschema():
    return {
        "type": "object",
        "properties": {
            "messages": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "role": {"type": "string", "enum": ["system", "user", "assistant"]},
                        "content": {"type": "string"}
                    },
                    "required": ["role", "content"]
                }
            },
            "model": {"type": "string", "default": MODEL_NAME},
            "temperature": {"type": "number", "default": 0.7},
            "max_tokens": {"type": "number", "default": 100}
        },
        "required": ["messages", "model"]
    }

# Function to get output JSON schema for the model
def get_output_jsonschema():
    return {
        "type": "object",
        "properties": {
            "choices": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "object",
                            "properties": {
                                "role": {"type": "string"},
                                "content": {"type": "string"}
                            }
                        }
                    }
                }
            }
        }
    }

# Print input and output JSON schemas
print("Input JSON Schema:")
print(get_input_jsonschema())

print("\nOutput JSON Schema:")
print(get_output_jsonschema())