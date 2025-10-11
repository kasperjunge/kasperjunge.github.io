import subprocess
from pathlib import Path

def serve():
    subprocess.run("uv run python tools/build.py", shell=True)
    subprocess.run("python -m http.server -d docs 8000", shell=True)

if __name__ == "__main__":
    serve()
