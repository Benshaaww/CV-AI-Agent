import os
from dotenv import load_dotenv

# Try loading .env
loaded = load_dotenv()
print(f"load_dotenv() returned: {loaded}")

# Check if key is set
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print("API Key found (starts with):", api_key[:5] + "...")
else:
    print("API Key NOT found.")

# Print current working directory
print("Current Working Directory:", os.getcwd())

# Check if .env file exists in CWD
print(".env exists in CWD:", os.path.exists(".env"))
