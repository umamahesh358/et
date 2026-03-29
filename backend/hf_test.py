import requests
import os
from dotenv import load_dotenv

load_dotenv()
hf_token = os.getenv("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {hf_token}"}
payload = {"inputs": "A beautiful news anchor desk, 4k"}

print(f"Token: {hf_token[:5]}...{hf_token[-5:]}")
print("Calling HF API...")
response = requests.post(API_URL, headers=headers, json=payload)
print("Status:", response.status_code)
if response.status_code != 200:
    print("Error:", response.text)
else:
    print("Success. Content len:", len(response.content))
