import re

def detect_language(code: str) -> str:
    code_lower = code.lower()

    scores = {
        "python": 0,
        "javascript": 0,
        "c": 0,
        "cpp": 0,
        "java": 0,
        "go": 0,
        "rust": 0,
        "php": 0,
        "bash": 0
    }

    # 🔹 PYTHON
    if re.search(r"\bdef\s+\w+\(", code): scores["python"] += 2
    if re.search(r"\bprint\s*\(", code): scores["python"] += 1
    if ":" in code and re.search(r"\n\s+", code): scores["python"] += 1
    if "self" in code_lower: scores["python"] += 1

    # 🔹 JAVASCRIPT
    if "console.log" in code: scores["javascript"] += 2
    if re.search(r"\bfunction\s+\w+", code): scores["javascript"] += 1
    if "=>" in code: scores["javascript"] += 2
    if "let " in code or "const " in code: scores["javascript"] += 1

    # 🔹 C
    if "#include" in code: scores["c"] += 2
    if re.search(r"\bprintf\s*\(", code): scores["c"] += 1
    if re.search(r"\bscanf\s*\(", code): scores["c"] += 1

    # 🔹 C++
    if "std::" in code: scores["cpp"] += 2
    if "cout" in code or "cin" in code: scores["cpp"] += 2
    if "#include <iostream>" in code: scores["cpp"] += 1

    # 🔹 JAVA
    if "public class" in code: scores["java"] += 2
    if "System.out.println" in code: scores["java"] += 2
    if "void main" in code: scores["java"] += 1

    # 🔹 GO
    if "package main" in code: scores["go"] += 2
    if "fmt." in code: scores["go"] += 1
    if re.search(r"func\s+\w+\(", code): scores["go"] += 2

    # 🔹 RUST
    if "fn main" in code: scores["rust"] += 2
    if "println!" in code: scores["rust"] += 2
    if "let mut" in code: scores["rust"] += 1

    # 🔹 PHP
    if "<?php" in code: scores["php"] += 2
    if "$" in code and "->" in code: scores["php"] += 1

    # 🔹 BASH
    if "#!/bin/bash" in code: scores["bash"] += 2
    if re.search(r"\becho\s+", code): scores["bash"] += 1
    if re.search(r"\bfi\b|\bthen\b", code): scores["bash"] += 1


    if re.search(r"\n\s{4,}", code) and ":" in code:
        scores["python"] += 1

    if code.count(";") > 3:
        scores["javascript"] += 1
        scores["c"] += 1
        scores["cpp"] += 1

    if "{" in code and "}" in code:
        scores["javascript"] += 1
        scores["c"] += 1
        scores["cpp"] += 1
        scores["java"] += 1

    # pick best match
    best_lang = max(scores, key=scores.get)

    # threshold check (avoid false positives)
    if scores[best_lang] == 0:
        return "unknown"

    return best_lang