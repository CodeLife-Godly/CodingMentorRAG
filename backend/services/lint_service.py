def run_linter(code, language):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as f:
            f.write(code.encode())
            file_path = f.name

        if language == "python":
            cmd = ["pylint", file_path]

        elif language == "javascript":
            cmd = ["eslint", file_path]

        elif language in ["c", "cpp"]:
            cmd = ["gcc", "-fsyntax-only", file_path]

        elif language == "java":
            cmd = ["javac", file_path]

        else:
            return "No linter configured for this language"

        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout + result.stderr

    except Exception as e:
        return str(e)