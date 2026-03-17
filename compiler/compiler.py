import subprocess
import tempfile
import os

# C 
def compile_c(code):

    if "main(" not in code:
        code = f"""
        #include <stdio.h>

        int main() {{
            {code}
            return 0;
        }}
        """

    with tempfile.NamedTemporaryFile(delete=False, suffix=".c") as temp:
        temp.write(code.encode())
        filename = temp.name

    result = subprocess.run(
        ["gcc", filename, "-o", filename + ".out"],
        capture_output=True,
        text=True
    )

    cleanup(filename)

    return clean_compiler_output(result.stderr)

# C++ 
def compile_cpp(code):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".cpp") as temp:
        temp.write(code.encode())
        filename = temp.name

    result = subprocess.run(
        ["g++", filename, "-o", filename + ".out"],
        capture_output=True,
        text=True
    )

    cleanup(filename)

    return clean_compiler_output(result.stderr)


# Python 
def compile_python(code):
    try:
        compile(code, "<string>", "exec")
        return "" 
    except Exception as e:
        return clean_compiler_output(str(e))


def cleanup(filename):
    if os.path.exists(filename):
        os.remove(filename)
    if os.path.exists(filename + ".out"):
        os.remove(filename + ".out")

def clean_compiler_output(output):
    lines = output.split("\n")

    error_lines = [line for line in lines if "error:" in line.lower()]

    return "\n".join(error_lines).strip()

def detect_language(code):

    code = code.strip()

    if "#include" in code:
        return "c"

    if "std::" in code or "cout" in code:
        return "cpp"

    if "def " in code or "print(" in code:
        return "python"

    return "unknown"


def run_compiler(code, language=None):

    lang = language if language else detect_language(code)

    if lang == "c":
        return compile_c(code)

    elif lang == "cpp":
        return compile_cpp(code)

    elif lang == "python":
        return compile_python(code)

    else:
        return "Unsupported language"