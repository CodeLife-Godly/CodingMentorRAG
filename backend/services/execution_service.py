import subprocess
import tempfile
import os

def run_code(code, language):
    try:
        if language == "python":
            suffix = ".py"
            cmd = ["python", "{file}"]

        elif language in ["javascript", "js"]:
            suffix = ".js"
            cmd = ["node", "{file}"]

        elif language == "c":
            suffix = ".c"
            cmd = ["bash", "-c", "gcc {file} -o {file}.out && {file}.out"]

        elif language == "cpp":
            suffix = ".cpp"
            cmd = ["bash", "-c", "g++ {file} -o {file}.out && {file}.out"]

        elif language == "java":
            suffix = ".java"
            cmd = ["bash", "-c", "javac {file} && java -cp {dir} Main"]

        elif language == "go":
            suffix = ".go"
            cmd = ["go", "run", "{file}"]

        elif language == "rust":
            suffix = ".rs"
            cmd = ["bash", "-c", "rustc {file} -o {file}.out && {file}.out"]

        elif language == "php":
            suffix = ".php"
            cmd = ["php", "{file}"]

        elif language == "bash":
            suffix = ".sh"
            cmd = ["bash", "{file}"]

        elif language == "typescript":
            suffix = ".ts"
            cmd = ["ts-node", "{file}"]

        else:
            return "Execution not supported for this language"

        # create temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
            f.write(code.encode())
            file_path = f.name

        # prepare command
        final_cmd = []
        for part in cmd:
            part = part.replace("{file}", file_path)
            part = part.replace("{dir}", os.path.dirname(file_path))
            final_cmd.append(part)

        try:
            result = subprocess.run(
                final_cmd,
                capture_output=True,
                text=True,
                timeout=5
            )
        except subprocess.TimeoutExpired:
            os.remove(file_path)
            return "Execution timed out (possible infinite loop)"

        os.remove(file_path)

        return (result.stdout or "") + (result.stderr or "")

    except Exception as e:
        return str(e)