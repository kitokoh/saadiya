import requests

access_token = 'your_facebook_access_token'
post_id = 'target_post_id'
comment = "Merci pour le partage! Découvrez notre logiciel Saadiya."

url = f'https://graph.facebook.com/{post_id}/comments'

data = {
    'message': comment,
    'access_token': access_token
}

response = requests.post(url, data=data)

if response.status_code == 200:
    print("Commentaire ajouté avec succès!")
else:
    print("Erreur lors de l'ajout du commentaire :", response.json())
