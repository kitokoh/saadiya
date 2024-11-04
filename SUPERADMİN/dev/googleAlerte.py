import smtplib
from email.mime.text import MIMEText

def send_email(subject, body):
    sender_email = "your_email@example.com"
    receiver_email = "receiver@example.com"
    password = "your_email_password"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email envoyé avec succès!")

# Utilisez cette fonction pour envoyer des alertes de mentions
send_email("Alerte de mention", "Votre logiciel a été mentionné sur un site!")
