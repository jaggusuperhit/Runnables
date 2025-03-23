import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenRouter API details
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = "gpt-3.5-turbo"  # Change this to the desired model name

# Input JSON schema
input_schema = {
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

# Output JSON schema
output_schema = {
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

# Print schemas
print("Input JSON Schema:", input_schema)
print("Output JSON Schema:", output_schema)
