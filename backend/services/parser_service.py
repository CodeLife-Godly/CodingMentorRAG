import re

def parse_code(code, language):
    lines = code.split("\n")

    functions = []
    loops = []
    conditionals = []
    nesting_depth = 0
    current_depth = 0

    for line in lines:
        stripped = line.strip()

        if language == "python":
            if re.match(r"def\s+\w+\(", stripped):
                functions.append(stripped)

            if re.match(r"(for|while)\s+", stripped):
                loops.append(stripped)

            if re.match(r"(if|elif|else)\s+", stripped):
                conditionals.append(stripped)

            if ":" in stripped:
                current_depth += 1

        elif language in ["javascript", "js"]:
            if re.search(r"function\s+\w+\(|=>", stripped):
                functions.append(stripped)

            if re.search(r"\b(for|while)\b", stripped):
                loops.append(stripped)

            if re.search(r"\b(if|else)\b", stripped):
                conditionals.append(stripped)

            current_depth += stripped.count("{") - stripped.count("}")

        elif language in ["c", "cpp"]:
            if re.search(r"\w+\s+\w+\(.*\)\s*\{", stripped):
                functions.append(stripped)

            if re.search(r"\b(for|while)\s*\(", stripped):
                loops.append(stripped)

            if re.search(r"\b(if|else)\s*\(", stripped):
                conditionals.append(stripped)

            current_depth += stripped.count("{") - stripped.count("}")

        elif language == "java":
            if re.search(r"(public|private|protected)?\s*\w+\s+\w+\(.*\)\s*\{", stripped):
                functions.append(stripped)

            if re.search(r"\b(for|while)\s*\(", stripped):
                loops.append(stripped)

            if re.search(r"\b(if|else)\s*\(", stripped):
                conditionals.append(stripped)

            current_depth += stripped.count("{") - stripped.count("}")

        elif language == "go":
            if re.search(r"func\s+\w+\(", stripped):
                functions.append(stripped)

            if re.search(r"\bfor\b", stripped):
                loops.append(stripped)

            if re.search(r"\bif\b", stripped):
                conditionals.append(stripped)

            current_depth += stripped.count("{") - stripped.count("}")

        elif language == "rust":
            if re.search(r"fn\s+\w+\(", stripped):
                functions.append(stripped)

            if re.search(r"\b(for|while|loop)\b", stripped):
                loops.append(stripped)

            if re.search(r"\bif\b", stripped):
                conditionals.append(stripped)

            current_depth += stripped.count("{") - stripped.count("}")

        elif language == "php":
            if re.search(r"function\s+\w+\(", stripped):
                functions.append(stripped)

            if re.search(r"\b(for|while|foreach)\b", stripped):
                loops.append(stripped)

            if re.search(r"\bif\b", stripped):
                conditionals.append(stripped)

            current_depth += stripped.count("{") - stripped.count("}")

        elif language == "bash":
            if re.search(r"\w+\s*\(\)\s*\{", stripped):
                functions.append(stripped)

            if re.search(r"\b(for|while)\b", stripped):
                loops.append(stripped)

            if re.search(r"\bif\b", stripped):
                conditionals.append(stripped)

            if re.search(r"\b(do|then)\b", stripped):
                current_depth += 1
            if re.search(r"\b(done|fi)\b", stripped):
                current_depth -= 1

        nesting_depth = max(nesting_depth, current_depth)

    return {
        "functions": functions,
        "loops": loops,
        "conditionals": conditionals,
        "lines": len(lines),
        "nesting_depth": nesting_depth
    }