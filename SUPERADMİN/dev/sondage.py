import requests

API_KEY = 'your_typeform_api_key'
url = "https://api.typeform.com/forms"

data = {
    "title": "Feedback sur Saadiya",
    "fields": [
        {
            "title": "Comment évaluez-vous notre logiciel ?",
            "type": "opinion_scale",
            "properties": {
                "steps": 5
            }
        },
        {
            "title": "Commentaires",
            "type": "long_text"
        }
    ]
}

response = requests.post(url, headers={'Authorization': f'Bearer {API_KEY}'}, json=data)

if response.status_code == 201:
    print("Sondage créé avec succès!")
else:
    print("Erreur lors de la création du sondage :", response.json())
