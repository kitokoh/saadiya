import requests

# Remplacez ces variables par vos propres données
username = "your_username"
password = "your_password"
url_to_share = "https://example.com/your-link"
description = "Description de votre lien"
tags = "tag1, tag2, tag3"

def share_on_delicious():
    api_url = "https://api.del.icio.us/v1/posts/add"
    payload = {
        'url': url_to_share,
        'description': description,
        'tags': tags,
        'login': username,
        'password': password
    }
    response = requests.post(api_url, data=payload)
    if response.status_code == 200:
        print("Partage réussi sur Delicious!")
    else:
        print("Erreur lors du partage sur Delicious:", response.content)

def share_on_diigo():
    api_url = "https://api.diigo.com/v2/add"
    payload = {
        'url': url_to_share,
        'title': description,
        'tags': tags,
        'login': username,
        'password': password
    }
    response = requests.post(api_url, data=payload)
    if response.status_code == 200:
        print("Partage réussi sur Diigo!")
    else:
        print("Erreur lors du partage sur Diigo:", response.content)

if __name__ == "__main__":
    share_on_delicious()
    share_on_diigo()
