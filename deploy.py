import subprocess


def deploy():

    subprocess.run(["uv", "run", "ablog", "build"])

    subprocess.run(["git", "add", "."])

    subprocess.run(["git", "commit", "-m", "update blog"])

    subprocess.run(
        [
            "uv", 
            "run", 
            "ablog", 
            "deploy", 
            "--github-branch", "main", 
            "-w", "docs", 
            "-g", "kasperjunge", 
            "-p", "docs"])

if __name__ == "__main__":
    deploy()