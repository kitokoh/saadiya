import json
import requests

API_KEY = 'your_mailchimp_api_key'
LIST_ID = 'your_mailchimp_list_id'
SERVER_PREFIX = 'usX'  # Remplacez X par votre serveur (ex: us1)

url = f'https://{SERVER_PREFIX}.api.mailchimp.com/3.0/lists/{LIST_ID}/members'

data = {
    "email_address": "user@example.com",
    "status": "subscribed",
    "merge_fields": {
        "FNAME": "First Name",
        "LNAME": "Last Name"
    }
}

response = requests.post(url, auth=('anystring', API_KEY), json=data)

if response.status_code == 200:
    print("Abonné ajouté avec succès à la liste!")
else:
    print("Erreur lors de l'ajout :", response.json())
