import os
import json

def load_json_data(json_file):
    """
    Charge les données à partir du fichier JSON.
    """
    if not json_file or not os.path.exists(json_file):
        return {'posts': []}

    with open(json_file, 'r') as f:
        return json.load(f)
def lighten_color(color):
    color = color.lstrip('#')
    r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
    r = min(255, int(r * 1.1))
    g = min(255, int(g * 1.1))
    b = min(255, int(b * 1.1))
    return f"#{r:02x}{g:02x}{b:02x}"

def save_json_data(json_file, media):
    """
    Sauvegarde la description d'un média dans le fichier JSON.
    """
    if not json_file:
        return

    # Charger les données existantes
    json_data = load_json_data(json_file)

    # Mise à jour ou ajout des informations sur le média
    for post in json_data['posts']:
        if post['image'] == media['preview_path']:
            post['text'] = media['description']
            break
    else:
        # Si le média n'existe pas encore dans le fichier JSON, l'ajouter
        json_data['posts'].append({
            'text': media['description'],
            'image': media['preview_path']
        })

    # Écriture des nouvelles données dans le fichier JSON
    with open(json_file, 'w') as f:
        json.dump(json_data, f, indent=4)
