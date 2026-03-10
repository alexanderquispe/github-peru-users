import subprocess
import os

def run_git_cmd(cmd):
    try:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")

os.chdir(r"c:\Users\Alexander\Documents\GitHub\github-peru-users")

# 1. Init
run_git_cmd(["git", "init"])

# 2. Add files
run_git_cmd(["git", "add", "."])

# 3. Commit
run_git_cmd(["git", "commit", "-m", "Initial commit: Peru GitHub Users Analysis"])

# 4. Remote
run_git_cmd(["git", "remote", "add", "origin", "https://github.com/alexanderquispe/github-peru-users.git"])

# 5. Branch
run_git_cmd(["git", "branch", "-M", "main"])

# 6. Status
run_git_cmd(["git", "status"])

print("Git setup complete (locally).")
