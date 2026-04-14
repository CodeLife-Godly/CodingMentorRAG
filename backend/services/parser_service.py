def parse_code(code, language):
    lines = code.split("\n")

    if language == "python":
        functions = [l for l in lines if l.strip().startswith("def ")]
        loops = [l for l in lines if "for " in l or "while " in l]

    elif language == "javascript":
        functions = [l for l in lines if "function " in l or "=>" in l]
        loops = [l for l in lines if "for " in l or "while " in l]

    elif language in ["c", "cpp", "java"]:
        functions = [l for l in lines if "(" in l and ")" in l and "{" in l]
        loops = [l for l in lines if "for(" in l or "while(" in l]

    else:
        functions = []
        loops = []

    return {
        "functions": functions,
        "loops": loops,
        "lines": len(lines)
    }