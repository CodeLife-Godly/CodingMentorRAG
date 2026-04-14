import requests
import os
import google.generativeai as genai
from config import OLLAMA_URL, OLLAMA_MODEL
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

os.environ["NO_PROXY"] = "localhost,127.0.0.1"
os.environ["no_proxy"] = "localhost,127.0.0.1"

def gemini_call(prompt: str) -> str:
    model = genai.GenerativeModel("models/gemini-2.5-flash")

    response = model.generate_content(prompt)

    return f"{response.text.strip()}"


def ollama_call(prompt: str) -> str:
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

    return f"{result}"


def query_llm(prompt: str) -> str:
    try:
        return gemini_call(prompt)

    except Exception as e:
        print("⚠️ Gemini failed, switching to Ollama:", e)

        try:
            return ollama_call(prompt)

        except Exception as ollama_error:
            return (
                "Both models failed:\n"
                f"Gemini: {str(e)}\n"
                f"Ollama: {str(ollama_error)}"
            )