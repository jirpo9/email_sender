import smtplib
import random
import time
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Načtení proměnných z .env souboru
load_dotenv()

# Kontrola povinných proměnných prostředí
REQUIRED = ("EMAIL_USER", "EMAIL_PASS", "RECIPIENT_EMAIL")
missing = [k for k in REQUIRED if not os.getenv(k)]
if missing:
    raise RuntimeError(f"❌ Chybějící proměnné v .env souboru: {', '.join(missing)}")

# Konfigurace emailu - načteno z .env
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SENDER_EMAIL = os.getenv("EMAIL_USER")
SENDER_PASSWORD = os.getenv("EMAIL_PASS")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

# Validace email formátu (základní)
def validate_email(email):
    """Základní validace email adresy"""
    return "@" in email and "." in email.split("@")[1]

if not all(validate_email(email) for email in [SENDER_EMAIL, RECIPIENT_EMAIL]):
    raise ValueError("❌ Neplatný formát email adresy")

# Definice kategorií a jejich obsahu
CATEGORIES = {
    "Mzdy": {
        "subjects": [
            "Výpočet mezd za měsíc {month}",
            "Dotaz k mzdovým nákladům",
            "Přehled mezd a odvodů",
            "Kontrola mzdových listů",
            "Změny v mzdovém účetnictví"
        ],
        "contents": [
            "Dobrý den,\n\nprosím o kontrolu výpočtu mezd za uplynulý měsíc. Přikládám mzdové listy k ověření.\n\nS pozdravem",
            "Zdravím,\n\nměl bych dotaz ohledně zaúčtování mzdových nákladů. Můžeme si domluvit konzultaci?\n\nDěkuji",
            "Dobrý den,\n\npotřebuji pomoc s přehledy mezd pro statistické úřady. Jaké údaje budeme potřebovat?\n\nS pozdravem",
            "Zdravím,\n\nprosím o kontrolu mzdových listů před odesláním zaměstnancům.\n\nDěkuji za rychlou odpověď",
            "Dobrý den,\n\ninformuji vás o změnách v mzdovém účetnictví od příštího měsíce.\n\nS pozdravem"
        ]
    },
    "Daně": {
        "subjects": [
            "Daňové přiznání za rok {year}",
            "DPH za měsíc {month}",
            "Silniční daň - dotaz",
            "Daň z příjmů právnických osob",
            "Kontrolní hlášení DPH"
        ],
        "contents": [
            "Dobrý den,\n\nprosím o přípravu daňového přiznání za minulý rok. Máte všechny potřebné doklady?\n\nS pozdravem",
            "Zdravím,\n\npotřebuji zkontrolovat výpočet DPH za uplynulý měsíc. Můžeme si projít čísla?\n\nDěkuji",
            "Dobrý den,\n\nmám dotaz ohledně výpočtu silniční daně pro naše vozidla.\n\nS pozdravem",
            "Zdravím,\n\npřipravujeme daň z příjmů PO. Prosím o zaslání potřebných podkladů.\n\nDěkuji",
            "Dobrý den,\n\npotřebujeme připravit kontrolní hlášení DPH. Máte připravené údaje?\n\nS pozdravem"
        ]
    },
    "Faktury": {
        "subjects": [
            "Neuhrazená faktura č. {number}",
            "Nová faktura k zaúčtování",
            "Dotaz k faktuře {number}",
            "Oprava na faktuře",
            "Žádost o zaplacení faktury"
        ],
        "contents": [
            "Dobrý den,\n\nupozorňuji na neuhrazenou fakturu s termínem splatnosti v minulém týdnu.\n\nS pozdravem",
            "Zdravím,\n\nposílám novou fakturu k zaúčtování. Prosím o zařazení do účetnictví.\n\nDěkuji",
            "Dobrý den,\n\nmám dotaz ohledně zaúčtování faktury. Můžeme si to vyjasnit?\n\nS pozdravem",
            "Zdravím,\n\nmusíme opravit chybu na vystavené faktuře. Jak postupovat?\n\nDěkuji",
            "Dobrý den,\n\nžádám o zaplacení faktury, která je již po splatnosti.\n\nS pozdravem"
        ]
    },
    "Rozpočet": {
        "subjects": [
            "Plánování rozpočtu na rok {year}",
            "Analýza rozpočtu Q{quarter}",
            "Překročení rozpočtu",
            "Revize rozpočtu",
            "Měsíční rozpočtová kontrola"
        ],
        "contents": [
            "Dobrý den,\n\nzačínáme plánovat rozpočet na příští rok. Můžeme si domluvit schůzku?\n\nS pozdravem",
            "Zdravím,\n\npotřebuji analýzu plnění rozpočtu za uplynulé čtvrtletí.\n\nDěkuji",
            "Dobrý den,\n\nv některých položkách jsme překročili plánovaný rozpočet. Můžeme to projednat?\n\nS pozdravem",
            "Zdravím,\n\nnavrhuju revizi rozpočtu na základě aktuálního vývoje.\n\nDěkuji",
            "Dobrý den,\n\nprosím o měsíční kontrolu plnění rozpočtu.\n\nS pozdravem"
        ]
    },
    "Pohledávky": {
        "subjects": [
            "Upomínka č. {number}",
            "Vymáhání pohledávky",
            "Analýza pohledávek",
            "Odpis nedobytné pohledávky",
            "Přehled splatných pohledávek"
        ],
        "contents": [
            "Dobrý den,\n\nposílám upomínku za neuhrazenou pohledávku po splatnosti.\n\nS pozdravem",
            "Zdravím,\n\npotřebujeme zahájit vymáhání dlouhodobě neuhrazené pohledávky.\n\nDěkuji",
            "Dobrý den,\n\nprosím o analýzu stavu našich pohledávek.\n\nS pozdravem",
            "Zdravím,\n\nnavrhuju odpis nedobytné pohledávky. Můžeme to projednat?\n\nDěkuji",
            "Dobrý den,\n\npotřebuji přehled všech splatných pohledávek.\n\nS pozdravem"
        ]
    },
    "Inventura": {
        "subjects": [
            "Příprava roční inventury",
            "Výsledky inventury skladu",
            "Inventurní rozdíly",
            "Plán inventury na rok {year}",
            "Dotaz k inventurním postupům"
        ],
        "contents": [
            "Dobrý den,\n\nzahajujeme přípravu roční inventury. Máte připravené postupy?\n\nS pozdravem",
            "Zdravím,\n\nposílám výsledky inventury skladu k zaúčtování.\n\nDěkuji",
            "Dobrý den,\n\nvznikly některé inventurní rozdíly. Jak je máme zaúčtovat?\n\nS pozdravem",
            "Zdravím,\n\npotřebujeme sestavit plán inventur na příští rok.\n\nDěkuji",
            "Dobrý den,\n\nmám dotaz ohledně správných inventurních postupů.\n\nS pozdravem"
        ]
    },
    "Dotace": {
        "subjects": [
            "Žádost o dotaci - projekt {name}",
            "Vyúčtování dotace",
            "Kontrola čerpání dotace",
            "Nová dotační příležitost",
            "Závěrečná zpráva o dotaci"
        ],
        "contents": [
            "Dobrý den,\n\npřipravujeme žádost o dotaci. Potřebujeme pomoct s finančním plánem.\n\nS pozdravem",
            "Zdravím,\n\nmusíme připravit vyúčtování čerpané dotace. Máte všechny doklady?\n\nDěkuji",
            "Dobrý den,\n\nprosím o kontrolu správnosti čerpání dotačních prostředků.\n\nS pozdravem",
            "Zdravím,\n\nobjevila se nová dotační příležitost. Mohli bychom ji využít?\n\nDěkuji",
            "Dobrý den,\n\npotřebujeme připravit závěrečnou zprávu o využití dotace.\n\nS pozdravem"
        ]
    },
    "Audit": {
        "subjects": [
            "Příprava na audit",
            "Auditní zjištění",
            "Požadavky auditora",
            "Nápravná opatření",
            "Dokumentace pro audit"
        ],
        "contents": [
            "Dobrý den,\n\nblíží se audit. Máme připravenou všechnu dokumentaci?\n\nS pozdravem",
            "Zdravím,\n\nauditor má některá zjištění. Musíme je projednat a vyřešit.\n\nDěkuji",
            "Dobrý den,\n\nauditor požaduje dodatečné dokumenty. Můžete je připravit?\n\nS pozdravem",
            "Zdravím,\n\nmusíme implementovat nápravná opatření podle doporučení auditora.\n\nDěkuji",
            "Dobrý den,\n\nprosím o přípravu dokumentace pro nadcházející audit.\n\nS pozdravem"
        ]
    },
    "Výkazy": {
        "subjects": [
            "Rozvaha za rok {year}",
            "Výkaz zisku a ztráty",
            "Přehled o peněžních tocích",
            "Měsíční výkazy",
            "Poznámky k účetní závěrce"
        ],
        "contents": [
            "Dobrý den,\n\npotřebujeme sestavit rozvahu za uplynulý rok. Máte připravené údaje?\n\nS pozdravem",
            "Zdravím,\n\nprosím o kontrolu výkazu zisku a ztráty před odesláním.\n\nDěkuji",
            "Dobrý den,\n\nchybí nám přehled o peněžních tocích. Můžete ho připravit?\n\nS pozdravem",
            "Zdravím,\n\npotřebujemes dokončit měsíční výkazy do konce týdne.\n\nDěkuji",
            "Dobrý den,\n\nmusíme připravit poznámky k účetní závěrce.\n\nS pozdravem"
        ]
    },
    "Bankovnictví": {
        "subjects": [
            "Odsouhlasení bankovních výpisů",
            "Bankovní poplatky",
            "Nový bankovní účet",
            "Přehled bankovních operací",
            "Problém s platbou"
        ],
        "contents": [
            "Dobrý den,\n\npotřebujeme odsouhlasit bankovní výpisy s účetnictvím.\n\nS pozdravem",
            "Zdravím,\n\nv bance nám naúčtovali neočekávané poplatky. Můžeme to zkontrolovat?\n\nDěkuji",
            "Dobrý den,\n\nzakládáme nový bankovní účet. Jak ho zavedeme do účetnictví?\n\nS pozdravem",
            "Zdravím,\n\npotřebuji přehled všech bankovních operací za minulý měsíc.\n\nDěkuji",
            "Dobrý den,\n\nvznikl problém s odchozí platbou. Můžete to vyřešit?\n\nS pozdravem"
        ]
    }
}

def generate_random_values():
    """Generuje náhodné hodnoty pro použití v předmětech a obsahu"""
    months = ["leden", "únor", "březen", "duben", "květen", "červen", 
              "červenec", "srpen", "září", "říjen", "listopad", "prosinec"]
    years = ["2023", "2024", "2025"]
    quarters = ["1", "2", "3", "4"]
    numbers = [f"{random.randint(1000, 9999)}" for _ in range(10)]
    names = ["Alpha", "Beta", "Gamma", "Delta", "Omega"]
    
    return {
        "month": random.choice(months),
        "year": random.choice(years),
        "quarter": random.choice(quarters),
        "number": random.choice(numbers),
        "name": random.choice(names)
    }

def send_email(subject, content, recipient):
    """Odešle jeden email s kompletním error handlingem"""
    try:
        # Vytvoření zprávy
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient
        msg['Subject'] = subject
        msg['Date'] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")
        
        # Přidání obsahu
        msg.attach(MIMEText(content, 'plain', 'utf-8'))
        
        # Připojení k SMTP serveru a odeslání
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("❌ Chyba ověření - zkontrolujte email a heslo (pro Gmail použijte App Password)")
        return False
    except smtplib.SMTPRecipientsRefused:
        print("❌ Neplatná cílová email adresa")
        return False
    except smtplib.SMTPServerDisconnected:
        print("❌ Připojení k SMTP serveru bylo přerušeno")
        return False
    except Exception as e:
        print(f"❌ Neočekávaná chyba při odesílání: {e}")
        return False

def main():
    """Hlavní funkce - odešle 50 emailů (5 pro každou kategorii)"""
    print("🚀 Zahajuji odesílání testovacích emailů...")
    print(f"📧 Odesílání z: {SENDER_EMAIL}")
    print(f"📥 Odesílání na: {RECIPIENT_EMAIL}")
    print(f"📊 Počet kategorií: {len(CATEGORIES)}")
    print(f"📈 Celkem emailů: {len(CATEGORIES) * 5}")
    print("=" * 60)
    
    # Potvrzení od uživatele
    confirmation = input("\n⚠️  Opravdu chcete odeslat všechny emaily? (ano/ne): ").lower().strip()
    if confirmation not in ['ano', 'a', 'yes', 'y']:
        print("❌ Odesílání zrušeno uživatelem")
        return
    
    sent_count = 0
    failed_count = 0
    start_time = datetime.now()
    
    for category_name, category_data in CATEGORIES.items():
        print(f"\n📂 Odesílám emaily pro kategorii: {category_name}")
        
        for i in range(5):  # 5 emailů pro každou kategorii
            # Generování náhodných hodnot
            random_values = generate_random_values()
            
            # Výběr náhodného předmětu a obsahu
            subject_template = random.choice(category_data["subjects"])
            content_template = random.choice(category_data["contents"])
            
            # Nahrazení placeholder hodnot
            try:
                subject = subject_template.format(**random_values)
            except KeyError as e:
                print(f"⚠️  Chyba v template předmětu: {e}")
                subject = subject_template
            
            content = content_template
            
            # Přidání kategorie do předmětu pro snadnější filtrování
            subject = f"[{category_name.upper()}] {subject}"
            
            # Přidání informací o kategorii do obsahu
            content += f"\n\n---\nKategorie: {category_name}\nEmail {i+1}/5 pro tuto kategorii\nOdesláno: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
            
            print(f"  📤 Email {i+1}/5: {subject[:50]}{'...' if len(subject) > 50 else ''}")
            
            # Odeslání emailu
            if send_email(subject, content, RECIPIENT_EMAIL):
                sent_count += 1
                print(f"  ✅ Úspěšně odesláno")
            else:
                failed_count += 1
                print(f"  ❌ Chyba při odesílání")
            
            # Pauza mezi emaily (aby nedošlo k omezení ze strany SMTP serveru)
            time.sleep(2)
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    print("\n" + "=" * 60)
    print("📊 SOUHRN ODESÍLÁNÍ:")
    print(f"✅ Úspěšně odesláno: {sent_count}")
    print(f"❌ Neúspěšně: {failed_count}")
    print(f"📋 Celkem: {sent_count + failed_count}")
    print(f"⏱️  Doba trvání: {duration}")
    print(f"📅 Dokončeno: {end_time.strftime('%d.%m.%Y %H:%M:%S')}")
    print("=" * 60)
    
    if sent_count > 0:
        print(f"\n✨ Zkontrolujte vaši emailovou schránku: {RECIPIENT_EMAIL}")
        print("💡 Tip: Emaily mohou být ve spam složce")

if __name__ == "__main__":
    try:
        print("🔧 KONTROLA KONFIGURACE:")
        print(f"📧 Odesílací email: {SENDER_EMAIL}")
        print(f"📥 Cílový email: {RECIPIENT_EMAIL}")
        print(f"🔗 SMTP server: {SMTP_SERVER}:{SMTP_PORT}")
        print("\n⚠️  DŮLEŽITÉ:")
        print("1. ✅ Ujistěte se, že máte správně nastaven .env soubor")
        print("2. ✅ Pro Gmail použijte App Password místo běžného hesla")
        print("3. ✅ Zkontrolujte, že máte povolený přístup k méně zabezpečeným aplikacím")
        print("\n🚀 Stiskněte Enter pro pokračování nebo Ctrl+C pro zrušení...")
        input()
        
        main()
        
    except KeyboardInterrupt:
        print("\n❌ Program byl přerušen uživatelem")
    except Exception as e:
        print(f"\n💥 Kritická chyba: {e}")
        print("🔍 Zkontrolujte vaši konfiguraci v .env souboru")