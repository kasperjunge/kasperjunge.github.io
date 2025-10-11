import subprocess
from pathlib import Path

def deploy():
    
    # 1. Get the path to the build directory
    build_path = str((Path(__file__).parent / "docs").resolve())

    # 2. Build the blog
    subprocess.run("uv run python tools/build.py", shell=True)

    # 3. Commit the blog updates
    subprocess.run("git add .", shell=True)
    subprocess.run('git commit -m "update blog"', shell=True)

    # 4. Deploy the blog to GitHub pages (via git push and GH Pages serving from docs/)
    # Keeping this as a simple push; Pages is configured to serve from docs/ on main

    # 5. Push the updates to the repository
    subprocess.run("git push", shell=True)

if __name__ == "__main__":
    deploy()
