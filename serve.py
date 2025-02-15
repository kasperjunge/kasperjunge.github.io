import subprocess
from pathlib import Path

def serve():
    subprocess.run("uv run ablog build -w docs", shell=True)
    subprocess.run("uv run ablog serve -r -w docs", shell=True)

if __name__ == "__main__":
    serve()
