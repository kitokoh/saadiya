from google.cloud import aiplatform

# Initialiser le client Vertex AI
project = "teak-mantis-433213-a4"  # Remplacez par votre ID de projet Google Cloud
location = "europe-west9"  # Remplacez par la région de votre endpoint, par exemple "us-central1"
endpoint_id = "votre-endpoint-id"  # Remplacez par l'ID de votre endpoint Vertex AI

# Initialise Vertex AI
aiplatform.init(project=project, location=location)

# Charger l'endpoint
endpoint = aiplatform.Endpoint(endpoint_name=endpoint_id)

# Préparer la fonction de prédiction
def predict(prompt):
    """Envoie une requête à l'endpoint Vertex AI et retourne la réponse au format JSON."""
    instances = [{"content": prompt}]
    parameters = {"temperature": 0.7}  # Ajuster les paramètres selon vos besoins

    # Envoyer la requête de prédiction
    response = endpoint.predict(instances=instances, parameters=parameters)
    # Extraire le résultat
    result = response.predictions[0]["content"]
    return {"response": result}

# Exemple d'utilisation
prompt = "Quel est le sens de la vie ?"
json_response = predict(prompt)
print(json_response)
