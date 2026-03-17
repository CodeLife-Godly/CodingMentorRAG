from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rag_engine.retrieve import retrieve_context
from llm_engine.llm import generate_answer
from compiler.compiler import run_compiler   

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/mentor")
def coding_mentor(data: dict):

    code = data["code"]
    language = data["language"]

    compiler_output = run_compiler(code, language)

    context = retrieve_context(code, language)

    answer = generate_answer(
        code,
        context,
        compiler_output,
        language,
    )

    return {
        "compiler_output": compiler_output,
        "retrieved_context": context,
        "mentor_response": answer
    }