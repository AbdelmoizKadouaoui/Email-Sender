import smtplib
from email.message import EmailMessage
import time
import random
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# ===== CONFIGURATION UTILISATEUR =====
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")  

SENDER_NAME = "Abdelmoiz Kadouaoui"
PDF_FILE_PATH = "Abdelmoiz kadouaoui PFE.pdf"  # ton CV (doit être dans le même dossier)

# === Configuration du message ===
SUBJECT = "Candidature - Stage PFE 2026"

EMAIL_BODY = f"""
<html>
<body style="font-family: Arial, sans-serif; color: #333;">
<p>Bonjour,</p>

<p>Je m'appelle Abdelmoiz Kadouaoui, élève ingénieur en 5ᵉ année à l'<strong>ENSA Khouribga</strong>.</p>

<p>Passionné par l'exploitation de technologies avancées pour créer de la valeur à partir des données,
je suis particulièrement intéressé par les domaines du <strong>Data Engineering</strong>, de la
<strong>Business Intelligence</strong> et de la <strong>Data Science</strong>.</p>

<p>Je suis toujours en quête de projets et de solutions concrètes pour transformer les données en leviers de performance et d'innovation.</p>

<p>Actuellement à la recherche d'un <strong>Stage PFE (4-6 mois)</strong> pour mettre en pratique mes compétences
et contribuer à des projets innovants, je vous adresse ma candidature pour un Stage PFE 2026,
disponible à partir de <strong>janvier/février 2026</strong>.</p>

<p>En pièce jointe, vous trouverez mon CV ainsi que mon portfolio :
<a href="https://protofilio-abdelmoizkadouaoui.vercel.app" target="_blank">
protofilio-abdelmoizkadouaoui.vercel.app
</a>.</p>

<p>Cordialement,<br>
{SENDER_NAME}
</p>
</body>
</html>
"""

# === Paramètres d'envoi ===
EMAIL_DELAY_MIN = 20       # délai minimum entre emails (en secondes)
EMAIL_DELAY_MAX = 40       # délai maximum entre emails
BATCH_DELAY_MIN = 300      # 5 à 7 minutes entre batchs x
BATCH_DELAY_MAX = 420
EMAILS_PER_BATCH = 15      # petite pause toutes les 25 pour éviter détection

EMAIL_LIST_FILE = "EmailList.txt"

# === Fonctions ===
def load_emails_from_file(file_path):
    """Lit les adresses e-mails depuis un fichier texte."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            emails = [line.strip() for line in f if line.strip()]
        if not emails:
            sys.exit("⚠️ Le fichier emails.txt est vide.")
        return emails
    except FileNotFoundError:
        sys.exit(f"❌ Fichier '{file_path}' introuvable.")
    except Exception as e:
        sys.exit(f"⚠️ Erreur de lecture du fichier : {e}")

def send_email(subject, html_body, to_email, pdf_file, smtp_session):
    """Envoie un e-mail HTML avec pièce jointe."""
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg["To"] = to_email
    msg.set_content("Veuillez activer l'affichage HTML pour lire ce message.")
    msg.add_alternative(html_body, subtype="html")

    # Attacher le CV
    try:
        with open(pdf_file, "rb") as f:
            pdf_data = f.read()
        msg.add_attachment(
            pdf_data,
            maintype="application",
            subtype="pdf",
            filename=os.path.basename(pdf_file),
        )
    except Exception as e:
        print(f"⚠️ Impossible d'attacher le fichier PDF : {e}")
        return False

    try:
        smtp_session.send_message(msg)
        print(f"✅ Email envoyé à {to_email}")
        return True
    except Exception as e:
        print(f"🚫 Erreur d'envoi ({to_email}) : {e}")
        return False

def main():
    recipients = load_emails_from_file(EMAIL_LIST_FILE)
    print(f"📧 {len(recipients)} adresses chargées depuis {EMAIL_LIST_FILE}")
    print("🚀 Début de l'envoi...\n")

    # Connexion SMTP
    smtp_session = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_session.starttls()
    smtp_session.login(SENDER_EMAIL, APP_PASSWORD)

    for i, recipient in enumerate(recipients, start=1):
        send_email(SUBJECT, EMAIL_BODY, recipient, PDF_FILE_PATH, smtp_session)

        # Attente entre les envois (délai aléatoire)
        if i < len(recipients):
            delay = random.randint(EMAIL_DELAY_MIN, EMAIL_DELAY_MAX)
            print(f"⏳ Attente de {delay} secondes avant le prochain envoi...")
            time.sleep(delay)

        # Petite pause de sécurité toutes les 25 adresses
        if i % EMAILS_PER_BATCH == 0 and i < len(recipients):
            batch_delay = random.randint(BATCH_DELAY_MIN, BATCH_DELAY_MAX)
            print(f"⏸️ Pause de {batch_delay} secondes avant la suite...")
            time.sleep(batch_delay)

    smtp_session.quit()
    print("\n✅ Tous les e-mails ont été envoyés avec succès !")

if __name__ == "__main__":
    main()
