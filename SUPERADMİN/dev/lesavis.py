import requests
import json

# Configuration de l'API Trustpilot
API_KEY = 'your_trustpilot_api_key'
BUSINESS_UNIT_ID = 'your_business_unit_id'  # Remplacez par l'ID de votre unité commerciale

# URL de l'API Trustpilot pour récupérer les avis
URL = f'https://api.trustpilot.com/v1/products/{BUSINESS_UNIT_ID}/reviews'

def fetch_reviews():
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Accept': 'application/json'
    }

    response = requests.get(URL, headers=headers)

    if response.status_code == 200:
        reviews = response.json()
        return reviews['reviews']  # Assurez-vous que la clé correspond à la réponse de l'API
    else:
        print(f"Failed to fetch reviews: {response.status_code} {response.text}")
        return []

def save_reviews_to_file(reviews):
    with open('trustpilot_reviews.json', 'w') as file:
        json.dump(reviews, file, indent=4)
        print("Reviews saved to trustpilot_reviews.json")

def main():
    reviews = fetch_reviews()
    if reviews:
        save_reviews_to_file(reviews)

if __name__ == "__main__":
    main()
