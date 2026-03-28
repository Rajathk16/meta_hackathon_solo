import sys
import subprocess
from pathlib import Path

def main():
    print("🚀 Auto-Deploy Script initialized...")

    print("\n📦 Ensuring deployment libraries are installed...")
    subprocess.run(["uv", "pip", "install", "huggingface_hub", "openenv-core"], check=True)

    print("\n🔑 Logging into Hugging Face automatically...")
    try:
        from huggingface_hub._login import login
        import os
        token = os.getenv("HF_TOKEN") or input("Please securely paste your new 'Write' HF Token and hit Enter: ").strip()
        login(token, add_to_git_credential=False)
        print("✅ Login successful!")
    except Exception as e:
        print("❌ Login failed:", e)
        return

    # Find the OpenEnv executable reliably
    import site
    paths = site.getsitepackages() + [site.getusersitepackages()]
    
    openenv_exe = None
    # Check sys.prefix first (standard virtual envs and UV)
    possible_exe = Path(sys.prefix) / "Scripts" / "openenv.exe"
    if possible_exe.exists():
        openenv_exe = str(possible_exe)
    else:
        # Fallback to site packages
        for p in paths:
            parent = Path(p).parent
            possible_exe = parent / "Scripts" / "openenv.exe"
            if possible_exe.exists():
                openenv_exe = str(possible_exe)
                break

    if not openenv_exe:
        print("\n❌ Could not find openenv.exe. Please ensure you are not missing permissions.")
        return

    print(f"\n✅ Found openenv deployment tool at: {openenv_exe}")
    
    try:
        from huggingface_hub import whoami
        username = whoami()["name"]
        print(f"\n👤 Authenticated automatically as: {username}")
    except Exception as e:
        username = input("\n👤 Could not fetch username from token. Please type your Hugging Face username: ")
        
    repo_id = f"{username}/openenv_email"

    print(f"\n🔥 Pushing environment to https://huggingface.co/spaces/{repo_id} ...")
    
    import os
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"

    try:
        subprocess.run([openenv_exe, "push", "--repo-id", repo_id], check=True, env=env)
        print("\n🎉 Deployment Triggered Successfully!")
        print(f"👉 Go grab your URL from Hugging Face and submit it!")
    except subprocess.CalledProcessError as e:
        print("\n❌ Deployment failed during push:", e)
        print("\n[IMPORTANT]: If you are seeing a 403 Forbidden error, your HF_TOKEN is likely set to 'Read' instead of 'Write'. Go to huggingface.co/settings/tokens and generate a new token with 'Write' permissions and replace it in your name.txt file!")

if __name__ == "__main__":
    main()
