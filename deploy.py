import subprocess

def deploy():

    print("------ Building blog...")
    subprocess.run("uv run ablog build", shell=True)
    
    print("\n------ Committing changes")
    subprocess.run("git add .", shell=True)
    subprocess.run('git commit -m "update blog"', shell=True)
    
    print("\n------ Pushing changes")
    subprocess.run("uv run ablog deploy --github-branch main -w /Users/kasperjunge/gitrepo/writing/kasperjunge.github.io/docs -g kasperjunge -p /Users/kasperjunge/gitrepo/writing/kasperjunge.github.io/docs", shell=True)

if __name__ == "__main__":
    deploy()
