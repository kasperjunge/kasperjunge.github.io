import subprocess

def deploy():

    print("Building blog...")
    subprocess.run("uv run ablog build", shell=True)
    
    print("\nCommitting changes")
    subprocess.run("git add .", shell=True)
    subprocess.run('git commit -m "update blog"', shell=True)
    
    print("\nPushing changes")
    subprocess.run("uv run ablog deploy --github-branch main -w docs -g kasperjunge -p docs", shell=True)

if __name__ == "__main__":
    deploy()
