import subprocess
from pathlib import Path

def deploy():
    
    # Get the path to the build directory
    build_path = str((Path(__file__).parent / "docs").resolve())

    # Build the blog
    subprocess.run("uv run ablog build -w docs", shell=True)

    # Commit the blog updates
    subprocess.run("git add .", shell=True)
    subprocess.run('git commit -m "update blog"', shell=True)

    # Deploy the blog to GitHub pages
    subprocess.run(
        f"uv run ablog deploy --github-branch main -w {build_path} -g kasperjunge -p {build_path}",
        shell=True
    )

    # Push the updates to the repository
    subprocess.run("git push", shell=True)

if __name__ == "__main__":
    deploy()
