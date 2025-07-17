import os
from dotenv import load_dotenv

load_dotenv()  # Loads API keys from .env

# Select LLM provider: "openai", "groq", or "openrouter"
LLM_PROVIDER = "groq"  # Switched to Groq for free usage

# Model names for each provider
MODEL_NAMES = {
    "openai": "gpt-4o-mini",  # Fixed invalid model name
    "groq": "meta-llama/llama-4-scout-17b-16e-instruct",
    "openrouter": "mistralai/mistral-small-3.2-24b-instruct"
}

# Base URLs if needed (optional for OpenAI & Groq, required for OpenRouter)
BASE_URLS = {
    "openai": None,
    "groq": None,
    "openrouter": "https://openrouter.ai/api/v1"
}

# API keys from environment variables
API_KEYS = {
    "openai": os.getenv("OPENAI_API_KEY"),
    "groq": os.getenv("GROQ_API_KEY"),
    "openrouter": os.getenv("OPENROUTER_API_KEY")
}
