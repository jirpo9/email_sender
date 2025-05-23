# 📧 Generátor testovacích emailů pro účetnictví

> Python skript pro automatické generování a odesílání testovacích emailů s různými účetními tématy. Ideální pro testování emailových filtrů a automatického třídění emailů v účetních firmách.

## 🎯 Účel projektu

Tento skript byl vytvořen pro testování automatického třídění emailů v účetních firmách. Generuje **50 realistických testovacích emailů** rozdělených do **10 kategorií** účetních témat.

## ✨ Funkce

- **50 testovacích emailů** (5 emailů pro každou kategorii)
- **10 účetních kategorií**: Mzdy, Daně, Faktury, Rozpočet, Pohledávky, Inventura, Dotace, Audit, Výkazy, Bankovnictví
- **Realistický obsah** s českými účetními termíny
- **Automatické označování** kategorií v předmětu emailu
- **Bezpečná konfigurace** pomocí .env souboru
- **Podpora Gmail, Outlook, Seznam.cz**
- **Pokročilé error handling** a logování

## 🛠️ Požadavky

- **Python 3.6+**
- **Email účet** s povoleným SMTP přístupem
- **Pro Gmail**: App Password (dvoufaktorové ověření)

## 🚀 Rychlý start

### 1. Klonování repozitáře
```bash
git clone https://github.com/jirpo9/email_sender.git
cd email_sender
```

### 2. Instalace závislostí
```bash
pip install -r requirements.txt
```

### 3. Konfigurace
```bash
# Zkopírujte ukázkový soubor
cp .env.example .env

# Upravte .env soubor s vašimi údaji
nano .env
```

### 4. Spuštění
```bash
python email_sender.py
```

## ⚙️ Konfigurace

### Vytvoření .env souboru

Vytvořte soubor `.env` v root složce projektu:

```env
# Email configuration
EMAIL_USER=vas_email@gmail.com
EMAIL_PASS=vase_app_heslo
RECIPIENT_EMAIL=cilovy_email@gmail.com

# Volitelné SMTP nastavení (výchozí: Gmail)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### 🔐 Nastavení Gmail (doporučeno)

1. **Zapněte dvoufaktorové ověření (2FA)**:
   - Jděte na [Google Account](https://myaccount.google.com/)
   - Zabezpečení → Ověření ve 2 krocích

2. **Vytvořte App Password**:
   - Zabezpečení → [Hesla aplikací](https://myaccount.google.com/apppasswords)
   - Vyberte "Pošta" → "Jiné"
   - Zadejte název → Vygenerovat
   - Zkopírujte 16-znakové heslo do `EMAIL_PASS`

## 📊 Kategorie emailů

| Kategorie | Příklady témat | Počet emailů |
|-----------|----------------|--------------|
| **💰 Mzdy** | Výpočet mezd, mzdové listy, odvody | 5 |
| **📋 Daně** | DPH, daňová přiznání, silniční daň | 5 |
| **🧾 Faktury** | Neuhrazené faktury, nové faktury | 5 |
| **📈 Rozpočet** | Plánování rozpočtu, analýzy | 5 |
| **💳 Pohledávky** | Upomínky, vymáhání pohledávek | 5 |
| **📦 Inventura** | Příprava inventury, inventurní rozdíly | 5 |
| **🎯 Dotace** | Žádosti o dotace, vyúčtování | 5 |
| **🔍 Audit** | Příprava na audit, auditní zjištění | 5 |
| **📊 Výkazy** | Rozvaha, výkaz zisku a ztráty | 5 |
| **🏦 Bankovnictví** | Bankovní výpisy, platby | 5 |

## 🔧 Podporované SMTP servery

### Gmail (výchozí)
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### Outlook/Hotmail
```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
```

### Seznam.cz
```env
SMTP_SERVER=smtp.seznam.cz
SMTP_PORT=587
```

##