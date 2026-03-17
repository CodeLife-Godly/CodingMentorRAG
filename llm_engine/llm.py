import requests
import os

os.environ["NO_PROXY"] = "localhost,127.0.0.1"

def generate_answer(code, context):

    prompt = f"""
    You are an expert C programming mentor.

    Analyze the code strictly.

    Only report real issues.

    Check ALL of the following:
    1. Syntax errors
    2. Logical errors
    3. Runtime errors (memory, pointers, bounds)
    4. Control flow mistakes

    Do NOT assume missing context.
    Do NOT ignore small syntax issues.
    Be precise and concise.

    Code={code}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model":"qwen2.5-coder",
            "prompt":prompt,
            "stream":False
        }
    )

    print("STATUS:", response.status_code)
    print("TEXT:", response.text)

    return response.json().get("response", "No response")