import requests

# Informations d'identification GitHub
GITHUB_TOKEN = "your_github_token"
REPO = "yourusername/yourrepo"

# Récupérer les informations de release
url = f"https://api.github.com/repos/{REPO}/releases"
headers = {"Authorization": f"token {GITHUB_TOKEN}"}
response = requests.get(url, headers=headers)
releases = response.json()

# Analyser les téléchargements
for release in releases:
    print(f"Release: {release['name']}")
    for asset in release['assets']:
        print(f"  Asset: {asset['name']} - Téléchargements: {asset['download_count']}")
