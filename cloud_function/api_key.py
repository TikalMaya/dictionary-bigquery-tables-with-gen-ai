import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.getcwd(), 'configs', '.env'))

def get_api_key(model_name):
    """
    Retrieves the API key for the given model.
    """
    api_keys = {
        "chatgpt": os.getenv("OPENAI_API_KEY"),
        "gemini": os.getenv("GEMINI_API_KEY"),
    }

    if model_name not in api_keys:
        raise ValueError(f"API key for model {model_name} is not configured.")

    return api_keys[model_name]
