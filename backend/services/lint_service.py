import subprocess
import tempfile
import os

def run_linter(code, language):
    try:
        suffix_map = {
            "python": ".py",
            "javascript": ".js",
            "js": ".js",
            "c": ".c",
            "cpp": ".cpp",
            "java": ".java",
            "go": ".go",
            "rust": ".rs",
            "php": ".php",
            "bash": ".sh"
        }

        if language not in suffix_map:
            return ""

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix_map[language]) as f:
            f.write(code.encode())
            file_path = f.name


        if language == "python":
            cmd = ["pylint", "--disable=all", "--enable=E", file_path]

        elif language in ["javascript", "js"]:
            cmd = ["eslint", file_path, "--no-eslintrc", "--quiet"]

        elif language == "c":
            cmd = ["gcc", "-fsyntax-only", file_path]

        elif language == "cpp":
            cmd = ["g++", "-fsyntax-only", file_path]

        elif language == "java":
            cmd = ["javac", file_path]

        elif language == "go":
            cmd = ["go", "vet", file_path]

        elif language == "rust":
            cmd = ["rustc", "--emit=metadata", file_path]

        elif language == "php":
            cmd = ["php", "-l", file_path]

        elif language == "bash":
            cmd = ["bash", "-n", file_path]

        result = subprocess.run(cmd, capture_output=True, text=True)

        os.remove(file_path)

        output = (result.stdout or "") + (result.stderr or "")


        lower = output.lower()

        if "eslint" in lower and ("config" in lower or "eslintrc" in lower):
            return ""

        if "not found" in lower or "is not recognized" in lower:
            return ""

        return output.strip()

    except Exception:
        return ""