import smtplib
import random
import time
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

# Načtení proměnných z .env souboru
load_dotenv()

# Kontrola povinných proměnných prostředí
REQUIRED = ("EMAIL_USER", "EMAIL_PASS", "RECIPIENT_EMAIL")
missing = [k for k in REQUIRED if not os.getenv(k)]
if missing:
    raise RuntimeError(f"❌ Chybějící proměnné v .env souboru: {', '.join(missing)}")

# Konfigurace emailu
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SENDER_EMAIL = os.getenv("EMAIL_USER")
SENDER_PASSWORD = os.getenv("EMAIL_PASS")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

# Validace email adresy
def validate_email(email):
    return "@" in email and "." in email.split("@")[1]

if not all(validate_email(email) for email in [SENDER_EMAIL, RECIPIENT_EMAIL]):
    raise ValueError("❌ Neplatný formát emailové adresy")

# Testovací šablony (zkrácený výpis pro ukázku)
CATEGORIES = {
    "Mzdy": {
        "subjects": ["Výpočet mezd za měsíc {month}"],
        "contents": ["Dobrý den,\n\nprosím o kontrolu výpočtu mezd za měsíc {month}.\n\nS pozdravem"]
    },
    "Faktury": {
        "subjects": ["Neuhrazená faktura č. {number}"],
        "contents": ["Upozorňuji na neuhrazenou fakturu č. {number}. Děkuji."]
    }
}

def generate_random_values():
    months = ["leden", "únor", "březen", "duben", "květen"]
    numbers = [str(random.randint(1000, 9999)) for _ in range(5)]
    return {
        "month": random.choice(months),
        "number": random.choice(numbers)
    }

def send_email(subject, content, recipient):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(content, 'plain', 'utf-8'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        return True

    except smtplib.SMTPAuthenticationError:
        print("❌ Chyba ověření – zkontrolujte heslo nebo App Password")
    except smtplib.SMTPRecipientsRefused:
        print("❌ Neplatná emailová adresa")
    except Exception as e:
        print(f"❌ Neočekávaná chyba: {e}")
    return False

def main():
    print("📨 Příprava na odeslání testovacích emailů...")
    print(f"📧 Odesílací email: {SENDER_EMAIL}")
    print(f"📥 Cílový email: {RECIPIENT_EMAIL}")
    print("=" * 50)

    confirmation = input("⚠️  Opravdu chcete odeslat všechny emaily? (ano/ne): ").strip().lower()
    if confirmation not in ["ano", "yes", "a", "y"]:
        print("❌ Odesílání zrušeno uživatelem.")
        return

    sent_count = 0
    failed_count = 0
    start_time = datetime.now()

    for category, data in CATEGORIES.items():
        print(f"\n📂 Kategorie: {category}")
        for i in range(5):
            values = generate_random_values()
            subject = data["subjects"][0].format(**values)
            content = data["contents"][0].format(**values)
            subject = f"[{category}] {subject}"

            print(f"  📤 {i+1}/5: {subject}")
            if send_email(subject, content, RECIPIENT_EMAIL):
                print("    ✅ Odesláno")
                sent_count += 1
            else:
                print("    ❌ Chyba")
                failed_count += 1

            time.sleep(2)

    duration = datetime.now() - start_time
    print("\n✅ HOTOVO")
    print(f"🟢 Odesláno: {sent_count}")
    print(f"🔴 Neúspěšné: {failed_count}")
    print(f"⏱️  Doba trvání: {duration}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Přerušeno uživatelem.")
