import subprocess
from pathlib import Path

def deploy():
    build_path = (Path(__file__).parent / "docs").resolve()
    build_str = str(build_path)
    subprocess.run("uv run ablog build -w docs", shell=True)
    subprocess.run("git add .", shell=True)
    subprocess.run('git commit -m "update blog"', shell=True)
    subprocess.run(
        f"uv run ablog deploy --github-branch main -w {build_str} -g kasperjunge -p {build_str}",
        shell=True
    )

if __name__ == "__main__":
    deploy()
