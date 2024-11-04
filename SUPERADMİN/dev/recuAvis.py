import smtplib
from email.mime.text import MIMEText

# Informations pour l'envoi d'e-mail
smtp_server = "smtp.gmail.com"
smtp_port = 587
email_address = "your_email@gmail.com"
email_password = "your_password"

def send_review_request(user_email):
    subject = "Nous aimerions votre avis sur Saadiya!"
    body = """
    Bonjour,

    Merci d'avoir choisi Saadiya! Nous espérons que notre logiciel répond à vos attentes.

    Nous vous serions reconnaissants de prendre un moment pour laisser un avis sur l'une de ces plateformes :
    - Capterra: https://www.capterra.com/reviews/saadiya
    - G2 Crowd: https://www.g2.com/products/saadiya/reviews

    Votre feedback est précieux et nous aide à améliorer notre produit.

    Merci beaucoup!

    Cordialement,
    L'équipe Saadiya
    """

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = user_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_address, email_password)
            server.sendmail(email_address, user_email, msg.as_string())
            print(f"E-mail de demande d'avis envoyé à {user_email} avec succès!")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail: {e}")

if __name__ == "__main__":
    # Liste d'emails d'utilisateurs pour tester le script
    user_emails = ["user1@example.com", "user2@example.com"]
    for email in user_emails:
        send_review_request(email)
