from database import get_db_connection
import smtplib
from email.mime.text import MIMEText
import requests
import json

# Modèle pour les notifications
class Notification:
    @staticmethod
    def envoyer_notification(destinataire, message, type_notification='email'):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO notifications (type, message, destinataire)
        VALUES (?, ?, ?)
        ''', (type_notification, message, destinataire))
        conn.commit()
        conn.close()

        if type_notification == 'email':
            Notification.envoyer_email(destinataire, "Notification", message)
        elif type_notification == 'fcm':
            Notification.envoyer_notification_push(destinataire, message)

    @staticmethod
    def envoyer_email(destinataire, sujet, message):
        try:
            msg = MIMEText(message)
            msg['Subject'] = sujet
            msg['From'] = 'votre_email@gmail.com'
            msg['To'] = destinataire

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login('votre_email@gmail.com', 'votre_mot_de_passe')
                server.sendmail('votre_email@gmail.com', destinataire, msg.as_string())
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email : {e}")

    @staticmethod
    def envoyer_notification_push(fcm_token, message):
        url = "https://fcm.googleapis.com/fcm/send"
        headers = {
            "Authorization": "key=VOTRE_CLE_FCM",
            "Content-Type": "application/json"
        }
        data = {
            "to": fcm_token,
            "notification": {
                "title": "Notification",
                "body": message
            }
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code != 200:
            print(f"Erreur lors de l'envoi de la notification push : {response.text}")

# Modèle pour les stocks
class Stock:
    @staticmethod
    def verifier_stocks():
        conn = get_db_connection()
        stocks = conn.execute('SELECT ingredient, quantite, seuil_alerte FROM stocks WHERE quantite <= seuil_alerte').fetchall()
        conn.close()
        for stock in stocks:
            message = f"Alerte de stock faible : {stock['ingredient']} (Quantité: {stock['quantite']}, Seuil: {stock['seuil_alerte']})"
            Notification.envoyer_notification("proprietaire@example.com", message, type_notification='email')