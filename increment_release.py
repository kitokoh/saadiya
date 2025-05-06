import json
import subprocess
import re
import os

# Chemins à adapter
EXE_PATH = "public/leopardo.exe"
VERSION_FILE = "version.json"
REPO = "ton-utilisateur/leopardo"  # Change ça !

def get_current_version():
    if not os.path.exists(VERSION_FILE):
        return "0.0"
    with open(VERSION_FILE, "r") as f:
        data = json.load(f)
    return data["version"]

def increment_version(version):
    major, minor = map(int, version.split("."))
    return f"{major}.{minor + 1}"

def create_github_release(new_version):
    tag = f"v{new_version}"
    print(f"📦 Création release GitHub : {tag}")
    subprocess.run(["gh", "release", "create", tag, EXE_PATH,
                    "--title", tag, "--notes", f"Version {tag}"], check=True)

def update_version_json(new_version):
    download_url = f"https://github.com/{REPO}/releases/download/v{new_version}/leopardo.exe"
    version_info = {
        "version": new_version,
        "url": download_url
    }
    with open(VERSION_FILE, "w") as f:
        json.dump(version_info, f, indent=2)
    print(f"📝 Fichier version.json mis à jour")

# def deploy_firebase():
#     print("🚀 Déploiement Firebase Hosting")
#     subprocess.run(["firebase", "deploy", "--only", "hosting"], check=True)
def deploy_firebase():
    print("🚀 Déploiement Firebase Hosting")
    result = subprocess.run(["firebase", "deploy", "--only", "hosting"], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    result.check_returncode()

def main():
    current = get_current_version()
    new_version = increment_version(current)
    print(f"🔁 Passage de {current} ➤ {new_version}")
    create_github_release(new_version)
    update_version_json(new_version)
    deploy_firebase()
    print(f"✅ Mise à jour complète terminée pour la version {new_version}")

if __name__ == "__main__":
    main()
