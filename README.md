# 📧 Generátor testovacích emailů pro účetnictví

Python skript pro automatické generování a odesílání testovacích emailů s různými účetními tématy. Ideální pro testování emailových filtrů a automatického třídění emailů v účetních firmách.

## 🎯 Účel projektu

Tento skript byl vytvořen pro testování automatického třídění emailů v účetních firmách. Generuje 50 realistických testovacích emailů rozdělených do 10 kategorií účetních témat.

## 📋 Funkce

- **50 testovacích emailů** (5 emailů pro každou kategorii)
- **10 účetních kategorií**: Mzdy, Daně, Faktury, Rozpočet, Pohledávky, Inventura, Dotace, Audit, Výkazy, Bankovnictví
- **Realistický obsah** s českými účetními termíny
- **Automatické označování** kategorií v předmětu emailu
- **Konfigurovatelné nastavení** SMTP serveru
- **Podpora Gmail, Outlook, Seznam.cz**

## 🔧 Požadavky

- **Python 3.6+** (všechny požadované moduly jsou součástí standardní knihovny)
- **Email účet** s povoleným SMTP přístupem
- **Pro Gmail**: App Password (dvoufaktorové ověření)

## 📦 Instalace

1. **Klonujte repozitář:**
```bash
git clone https://github.com/vase-jmeno/email-tester.git
cd email-tester
```

2. **Vytvořte virtuální prostředí (volitelné):**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# nebo
venv\Scripts\activate     # Windows
```

3. **Nainstalujte závislosti:**
```bash
pip install -r requirements.txt
```

## ⚙️ Konfigurace

1. **Otevřete soubor** `email_sender.py`
2. **Upravte konfiguraci** v horní části:

```python
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "vas_email@gmail.com"      # Změňte na váš odesílací email
SENDER_PASSWORD = "vase_app_heslo"        # App Password pro Gmail
RECIPIENT_EMAIL = "cilovy_email@gmail.com" # Kde chcete emaily přijímat
```

### 🔐 Nastavení Gmail (doporučeno)

1. **Zapněte dvoufaktorové ověření (2FA)**:
   - Jděte na https://myaccount.google.com/
   - Zabezpečení → Ověření ve 2 krocích

2. **Vytvořte App Password**:
   - Zabezpečení → Hesla aplikací
   - Vyberte "Pošta" → "Jiné"
   - Zadejte název → Vygenerovat
   - Zkopírujte 16-znakové heslo

3. **Použijte App Password** místo běžného hesla

## 🚀 Spuštění

```bash
python email_sender.py
```

Program vás upozorní na potřebné nastavení a požádá o potvrzení před odesláním.

## 📊 Kategorie emailů

| Kategorie | Příklady témat |
|-----------|----------------|
| **Mzdy** | Výpočet mezd, mzdové listy, odvody |
| **Daně** | DPH, daňová přiznání, silniční daň |
| **Faktury** | Neuhrazené faktury, nové faktury |
| **Rozpočet** | Plánování rozpočtu, analýzy |
| **Pohledávky** | Upomínky, vymáhání pohledávek |
| **Inventura** | Příprava inventury, inventurní rozdíly |
| **Dotace** | Žádosti o dotace, vyúčtování |
| **Audit** | Příprava na audit, auditní zjištění |
| **Výkazy** | Rozvaha, výkaz zisku a ztráty |
| **Bankovnictví** | Bankovní výpisy, platby |

## 🔧 Podporované SMTP servery

### Gmail
```python
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

### Outlook/Hotmail
```python
SMTP_SERVER = "smtp-mail.outlook.com"
SMTP_PORT = 587
```

### Seznam.cz
```python
SMTP_SERVER = "smtp.seznam.cz"
SMTP_PORT = 587
```

## 🛠️ Přizpůsobení

### Změna počtu emailů na kategorii
```python
for i in range(5):  # Změňte 5 na požadovaný počet
```

### Přidání vlastní kategorie
```python
CATEGORIES["Nova_Kategorie"] = {
    "subjects": ["Předmět 1", "Předmět 2"],
    "contents": ["Obsah 1", "Obsah 2"]
}
```

## 🐛 Řešení problémů

### "Python není rozpoznán"
- Přeinstalujte Python s volbou "Add to PATH"

### "Authentication failed"
- Zkontrolujte App Password
- Ujistěte se, že máte zapnuté 2FA

### Emaily nedorazí
- Zkontrolujte spam složku
- Počkejte 5-10 minut
- Ověřte SMTP nastavení

### "Connection refused"
- Zkuste port 465 místo 587
- Zkontrolujte firewall/antivirus

## ⚠️ Bezpečnost

- **Nikdy necommitujte hesla** do Git repozitáře
- **Používejte App Password** místo hlavního hesla
- **Po testování** můžete App Password smazat
- **Používejte separátní testovací účty**

## 📄 Licence

MIT License - viz [LICENSE](LICENSE) soubor

## 🤝 Přispívání

1. Forkněte projekt
2. Vytvořte feature branch (`git checkout -b feature/nova-funkce`)
3. Commitněte změny (`git commit -am 'Přidání nové funkce'`)
4. Pushněte branch (`git push origin feature/nova-funkce`)
5. Otevřete Pull Request

## 📞 Kontakt

- **Autor**: Vaše Jméno
- **Email**: vas.email@example.com
- **GitHub**: [@vase-github-jmeno](https://github.com/vase-github-jmeno)

## 🙏 Poděkování

Děkuji všem, kteří přispěli k vývoju tohoto projektu a poskytli zpětnou vazbu.

---

**⚡ Tip**: Před prvním spuštěním si vytvořte záložní kopii důležitých emailů!