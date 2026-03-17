import requests
import os

os.environ["NO_PROXY"] = "localhost,127.0.0.1"

def generate_answer(code, context, compiler_output, language="general"):

    lang_map = {
        "c": "C",
        "cpp": "C++",
        "python": "Python"
    }

    lang_name = lang_map.get(language, "programming")

    prompt = f"""
You are an expert {lang_name} programming mentor.

Relevant programming knowledge:
{context}

The following compiler output is provided for internal analysis.
Do NOT display it in your response.
Use it only to understand errors.

Compiler Output:
{compiler_output}

Analyze the code strictly.

RULES:

1. If compiler output is NOT empty:
   - Explain ONLY the errors indicated by the compiler
   - Do NOT add new issues

2. If compiler output IS empty:
   - Analyze the code for logical errors
   - If no issues are found then return no issues found

GENERAL CONSTRAINTS:
- You MUST point to the exact code snippet from the given code
- Do NOT generate or modify code
- Do NOT assume missing parts
- Do NOT give corrected code
- Do NOT include compiler messages, file paths, or warnings in output

FORMAT RULES (VERY STRICT):
- Output MUST be valid Markdown
- Each field MUST be on a new line
- Do NOT merge fields
- Use EXACT headings

code = {code}

"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5-coder",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2
            }
        }
    )

    return response.json().get("response", "No response")