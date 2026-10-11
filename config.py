import os
from dotenv import load_dotenv

load_dotenv()

_raw_api_key = os.getenv("GROQ_API_KEY", "").strip()
GROQ_API_KEY = "" if _raw_api_key.lower() in {
    "", "your_groq_api_key_here", "your_real_key", "your_api_key_here"
} else _raw_api_key
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b").strip()
MAX_RETRIES = max(0, int(os.getenv("MAX_RETRIES", "2")))
