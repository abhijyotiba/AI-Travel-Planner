from configuration.config import LLM_PROVIDER, MODEL_NAMES, API_KEYS, BASE_URLS
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

def load_llm():
    provider = LLM_PROVIDER
    model_name = MODEL_NAMES[provider]
    api_key = API_KEYS[provider]
    base_url = BASE_URLS[provider]

    if provider == "groq":
        print("Loading Groq model...")
        return ChatGroq(model=model_name, api_key=api_key)
    
    elif provider == "openai":
        print("Loading OpenAI model...")
        return ChatOpenAI(model_name=model_name, api_key=api_key)
    
    elif provider == "openrouter":
        print("Loading OpenRouter model...")
        return ChatOpenAI(model_name=model_name, api_key=api_key, base_url=base_url)

    else:
        raise ValueError(f"Unknown LLM provider: {provider}")
