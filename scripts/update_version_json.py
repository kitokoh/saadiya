import json
import sys

version = sys.argv[1]
release_url = f"https://github.com/TON-USER/leopardo/releases/download/v{version}/leopardo.exe"

version_info = {
    "version": version,
    "url": release_url
}

with open("public/version.json", "w") as f:
    json.dump(version_info, f, indent=2)

print("version.json mis à jour")
