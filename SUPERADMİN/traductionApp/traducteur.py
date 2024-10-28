import os
import xml.etree.ElementTree as ET
from google.cloud import translate
from google.api_core.exceptions import GoogleAPICallError, InvalidArgument

# Assurez-vous que la variable d'environnement GOOGLE_APPLICATION_CREDENTIALS est définie
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\ibrahim\\Downloads\\ozcanweb\\credantial.json"

def traduire_fichier_ts(fichier_source, fichier_cible, langue_cible):
    # Initialiser le client de traduction
    translate_client = translate.TranslationServiceClient()

    # Charger le fichier .ts
    try:
        tree = ET.parse(fichier_source)
        root = tree.getroot()
        print(f"Fichier {fichier_source} chargé avec succès.")
    except ET.ParseError as e:
        print(f"Erreur lors de l'analyse du fichier {fichier_source}: {e}")
        return
    except FileNotFoundError:
        print(f"Le fichier {fichier_source} est introuvable.")
        return

    # Traduire chaque texte source
    try:
        messages = root.findall('.//message')
        texts_to_translate = [message.find('source').text for message in messages if message.find('source') is not None]

        if not texts_to_translate:
            print("Aucun texte à traduire trouvé dans le fichier.")
            return

        # Affichage des textes à traduire pour vérification
        print(f"Textes à traduire : {texts_to_translate}")

        # Traduire en lot si des textes existent
        response = translate_client.translate_text(
            contents=texts_to_translate,
            target_language_code=langue_cible,
            parent="projects/teak-mantis-433213-a4/locations/global"  # Remplacez par votre ID de projet Google Cloud
        )

        if not response.translations:
            print("Aucune traduction n'a été retournée par l'API.")
            return

        # Mettre à jour les traductions dans le fichier XML
        for message, translation in zip(messages, response.translations):
            if translation.translated_text:
                message.find('translation').text = translation.translated_text
                print(f"Texte traduit : {translation.translated_text}")
            else:
                print(f"Texte non traduit pour: {message.find('source').text}")

        # Enregistrer le fichier traduit
        tree.write(fichier_cible, encoding='utf-8', xml_declaration=True)
        print(f"Fichier traduit enregistré sous: {fichier_cible}")

    except GoogleAPICallError as e:
        print(f"Erreur d'appel API Google: {e}")
    except InvalidArgument as e:
        print(f"Argument invalide: {e}")
    except Exception as e:
        print(f"Erreur inattendue: {e}")

# Exemple d'utilisation
if __name__ == "__main__":
    # Utilisation du script via la ligne de commande
    import sys
    if len(sys.argv) != 4:
        print("Usage: python traducteur.py <fichier_source> <fichier_cible> <langue_cible>")
    else:
        fichier_source = sys.argv[1]
        fichier_cible = sys.argv[2]
        langue_cible = sys.argv[3]
        
        # Vérifier si le fichier source existe
        if not os.path.exists(fichier_source):
            print(f"Le fichier source {fichier_source} est introuvable.")
        else:
            traduire_fichier_ts(fichier_source, fichier_cible, langue_cible)
