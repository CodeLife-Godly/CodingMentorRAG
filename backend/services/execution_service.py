import subprocess
import tempfile
import os
import re

def run_code(code, language):
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
            "bash": ".sh",
            "typescript": ".ts"
        }

        if language not in suffix_map:
            return "Execution not supported for this language"

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix_map[language]) as f:
            f.write(code.encode())
            file_path = f.name

        dir_path = os.path.dirname(file_path)
        base_name = os.path.splitext(os.path.basename(file_path))[0]


        if language == "python":
            cmd = ["python", file_path]

        elif language in ["javascript", "js"]:
            cmd = ["node", file_path]

        elif language == "c":
            cmd = ["bash", "-c", f"gcc {file_path} -o {dir_path}/{base_name} && {dir_path}/{base_name}"]

        elif language == "cpp":
            cmd = ["bash", "-c", f"g++ {file_path} -o {dir_path}/{base_name} && {dir_path}/{base_name}"]

        elif language == "java":
            match = re.search(r'class\s+(\w+)', code)
            class_name = match.group(1) if match else "Main"

            java_file = os.path.join(dir_path, f"{class_name}.java")

            os.rename(file_path, java_file)

            cmd = ["bash", "-c", f"javac {java_file} && java -cp {dir_path} {class_name}"]

            file_path = java_file  

        elif language == "go":
            cmd = ["go", "run", file_path]

        elif language == "rust":
            cmd = ["bash", "-c", f"rustc {file_path} -o {dir_path}/{base_name} && {dir_path}/{base_name}"]

        elif language == "php":
            cmd = ["php", file_path]

        elif language == "bash":
            cmd = ["bash", file_path]

        elif language == "typescript":
            cmd = ["bash", "-c", f"ts-node {file_path}"]

        else:
            return "Execution not supported"

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=5
            )
        except subprocess.TimeoutExpired:
            return "Execution timed out (possible infinite loop)"

        try:
            os.remove(file_path)
        except:
            pass

        return (result.stdout or "") + (result.stderr or "")

    except Exception as e:
        return str(e)