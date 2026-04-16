import requests
import os
from config import OLLAMA_URL, OLLAMA_MODEL

os.environ["NO_PROXY"] = "localhost,127.0.0.1"
os.environ["no_proxy"] = "localhost,127.0.0.1"


def ollama_call(prompt: str) -> str:
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=60,
            proxies={"http": "", "https": ""}
        )

        if response.status_code != 200:
            raise Exception(f"{response.status_code} | {response.text}")

        data = response.json()
        result = data.get("response", "").strip()

        return result

    except Exception as e:
        return f"Ollama error: {str(e)}"


def query_llm(prompt: str) -> str:
    return ollama_call(prompt)