from fastapi import APIRouter
from services.lint_service import run_linter
from services.rag_service import get_rag_context
from services.ollama_service import query_llm
from services.execution_service import run_code
from services.parser_service import parse_code
from utils.language_detector import detect_language
from utils.prompt_builder import build_prompt

router = APIRouter()

@router.post("/analyze")
async def analyze_code(data: dict):
    code = data["code"]
    mode = data["mode"]

    language = detect_language(code)

    lint_output = run_linter(code, language)
    parsed = parse_code(code, language)
    runtime_output = run_code(code, language)
    rag_context = get_rag_context(code)

    prompt = build_prompt(
        code,
        lint_output,
        runtime_output,
        rag_context,
        parsed,
        mode
    )

    response = query_llm(prompt)

    return {
        "language": language,
        "analysis": response
    }