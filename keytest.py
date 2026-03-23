from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("CLAUDE_API_KEY", "").strip()
print(repr(api_key))
