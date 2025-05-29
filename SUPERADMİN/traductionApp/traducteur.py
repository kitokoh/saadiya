# import os
# import xml.etree.ElementTree as ET
# from google.api_core.exceptions import GoogleAPICallError, InvalidArgument
# from google.cloud import translate

# # Assurez-vous que la variable d'environnement GOOGLE_APPLICATION_CREDENTIALS est définie
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\ibrahim\\Downloads\\ozcanweb\\credantial.json"

# def traduire_fichier_ts(fichier_source, fichier_cible, langue_cible):
#     # Initialiser le client de traduction
#     translate_client = translate.TranslationServiceClient()

#     # Charger le fichier .ts
#     try:
#         tree = ET.parse(fichier_source)
#         root = tree.getroot()
#         print(f"Fichier {fichier_source} chargé avec succès.")
#     except ET.ParseError as e:
#         print(f"Erreur lors de l'analyse du fichier {fichier_source}: {e}")
#         return
#     except FileNotFoundError:
#         print(f"Le fichier {fichier_source} est introuvable.")
#         return

#     # Traduire chaque texte source
#     try:
#         messages = root.findall('.//message')
#         texts_to_translate = [message.find('source').text for message in messages if message.find('source') is not None]

#         if not texts_to_translate:
#             print("Aucun texte à traduire trouvé dans le fichier.")
#             return

#         # Affichage des textes à traduire pour vérification
#         print(f"Textes à traduire : {texts_to_translate}")

#         # Traduire en lot si des textes existent
#         response = translate_client.translate_text(
#             contents=texts_to_translate,
#             target_language_code=langue_cible,
#             parent="projects/teak-mantis-433213-a4/locations/global"  # Remplacez par votre ID de projet Google Cloud
#         )

#         if not response.translations:
#             print("Aucune traduction n'a été retournée par l'API.")
#             return

#         # Mettre à jour les traductions dans le fichier XML
#         for message, translation in zip(messages, response.translations):
#             if translation.translated_text:
#                 message.find('translation').text = translation.translated_text
#                 print(f"Texte traduit : {translation.translated_text}")
#             else:
#                 print(f"Texte non traduit pour: {message.find('source').text}")

#         # Enregistrer le fichier traduit
#         tree.write(fichier_cible, encoding='utf-8', xml_declaration=True)
#         print(f"Fichier traduit enregistré sous: {fichier_cible}")

#     except GoogleAPICallError as e:
#         print(f"Erreur d'appel API Google: {e}")
#     except InvalidArgument as e:
#         print(f"Argument invalide: {e}")
#     except Exception as e:
#         print(f"Erreur inattendue: {e}")

# # Exemple d'utilisation
# if __name__ == "__main__":
#     # Utilisation du script via la ligne de commande
#     import sys
#     if len(sys.argv) != 4:
#         print("Usage: python traducteur.py <fichier_source> <fichier_cible> <langue_cible>")
#     else:
#         fichier_source = sys.argv[1]
#         fichier_cible = sys.argv[2]
#         langue_cible = sys.argv[3]
        
#         # Vérifier si le fichier source existe
#         if not os.path.exists(fichier_source):
#             print(f"Le fichier source {fichier_source} est introuvable.")
#         else:
#             traduire_fichier_ts(fichier_source, fichier_cible, langue_cible)


import os
import sys
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from google.api_core.exceptions import GoogleAPICallError, RetryError
from google.cloud import translate_v2 as translate
from tqdm import tqdm  # Pour les barres de progression

class TSFileTranslator:
    def __init__(self):
        self.client = self.initialize_translation_client()
        
    def initialize_translation_client(self):
        """Initialise le client de traduction avec vérification des credentials"""
        try:
            # Vérification du fichier de credentials
            creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
            if not os.path.exists(creds_path):
                raise FileNotFoundError(f"Fichier de credentials introuvable : {creds_path}")
                
            return translate.Client()
        except Exception as e:
            print(f"Erreur d'initialisation du client : {e}")
            sys.exit(1)

    def validate_ts_file(self, file_path):
        """Valide la structure du fichier TS"""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            if root.tag != 'TS':
                raise ValueError("Le fichier n'est pas un fichier TS valide")
            return tree, root
        except ET.ParseError as e:
            print(f"Erreur XML dans le fichier {file_path} : {e}")
            return None, None
        except Exception as e:
            print(f"Erreur de validation : {e}")
            return None, None

    def translate_batch(self, texts, target_lang):
        """Traduction par lots avec gestion des erreurs"""
        try:
            results = self.client.translate(
                texts,
                target_language=target_lang,
                format_='text',  # Important pour le format Qt
                model='nmt'  # Utilisation du modèle Neural Machine Translation
            )
            return [result['translatedText'] for result in results]
        except (GoogleAPICallError, RetryError) as e:
            print(f"Erreur API Google: {e.message}")
            return None

    def process_message(self, message, translation_text):
        """Met à jour un message avec sa traduction"""
        translation = message.find('translation')
        if translation is None:
            translation = ET.SubElement(message, 'translation')
        translation.text = translation_text
        translation.set('type', 'finished')  # Marque comme traduction complète

    def translate_file(self, source_path, target_path, target_lang):
        """Traduit un fichier TS complet"""
        tree, root = self.validate_ts_file(source_path)
        if not tree:
            return False

        messages = root.findall('.//message')
        if not messages:
            print("Aucun message à traduire trouvé")
            return False

        # Préparation des textes
        sources = []
        for message in messages:
            source = message.find('source')
            if source is not None and source.text:
                sources.append(source.text)

        # Traduction par lots (max 128 éléments par requête)
        batch_size = 128
        translated_texts = []
        
        with ThreadPoolExecutor() as executor:
            futures = []
            for i in range(0, len(sources), batch_size):
                batch = sources[i:i + batch_size]
                futures.append(executor.submit(self.translate_batch, batch, target_lang))
            
            for future in tqdm(futures, desc="Traduction en cours", unit="batch"):
                result = future.result()
                if result:
                    translated_texts.extend(result)

        # Vérification du nombre de traductions
        if len(translated_texts) != len(sources):
            print("Erreur : Nombre de traductions incorrect")
            return False

        # Mise à jour du fichier
        for message, translated_text in zip(messages, translated_texts):
            self.process_message(message, translated_text)

        # Sauvegarde avec encodage UTF-8 et déclaration XML
        tree.write(target_path, encoding='utf-8', xml_declaration=True)
        print(f"\nTraduction terminée : {target_path}")
        return True

def main():
    if len(sys.argv) != 4:
        print("Usage: python traducteur.py <fichier_source.ts> <fichier_cible.ts> <langue_cible>")
        print("Exemple: python traducteur.py source.ts translated_fr.ts fr")
        return

    source_file = sys.argv[1]
    target_file = sys.argv[2]
    target_lang = sys.argv[3]

    if not os.path.exists(source_file):
        print(f"Erreur: Le fichier source {source_file} n'existe pas")
        return

    translator = TSFileTranslator()
    success = translator.translate_file(source_file, target_file, target_lang)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()