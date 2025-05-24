# 🤝 Přispívání do projektu

Děkujeme za váš zájem o přispívání do projektu **Generátor testovacích emailů pro účetnictví**! Tato příručka vám pomůže se začleněním do našeho projektu.

## 📋 Obsah

- [Kód chování](#-kód-chování)
- [Jak přispět](#-jak-přispět)
- [Typy příspěvků](#-typy-příspěvků)
- [Vývojové prostředí](#️-vývojové-prostředí)
- [Proces review](#-proces-review)
- [Coding standards](#-coding-standards)
- [Hlášení chyb](#-hlášení-chyb)
- [Návrhy vylepšení](#-návrhy-vylepšení)

## 🤖 Kód chování

Tento projekt se řídí [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/). Účastí na projektu se zavazujete dodržovat tyto standardy.

## 🚀 Jak přispět

### 1. Fork repozitáře
```bash
# Forkněte repozitář na GitHubu a poté:
git clone https://github.com/VAS_USERNAME/email_sender.git
cd email_sender
```

### 2. Vytvoření nové větve
```bash
git checkout -b feature/vase-nova-funkce
# nebo
git checkout -b fix/oprava-chyby
```

### 3. Nastavení vývojového prostředí
```bash
# Vytvoření virtuálního prostředí
python -m venv venv
source venv/bin/activate  # Linux/Mac
# nebo
venv\Scripts\activate     # Windows

# Instalace závislostí
pip install -r requirements.txt

# Kopírování konfiguračního souboru
cp .env.example .env
# Upravte .env podle vašich potřeb
```

### 4. Provedení změn
- Implementujte vaše změny
- Otestujte funkcionalitu
- Přidejte komentáře k složitějšímu kódu

### 5. Commit a push
```bash
git add .
git commit -m "feat: přidání nové funkce XYZ"
git push origin feature/vase-nova-funkce
```

### 6. Vytvoření Pull Requestu
- Otevřete Pull Request na GitHubu
- Použijte popisný název a detailní popis
- Připojte screenshoty/logy pokud je to relevantní

## 📝 Typy příspěvků

### 🐛 Opravy chyb (Bug fixes)
- Opravujte reportované issue
- Přidejte testy pokud je to možné
- Ověřte, že oprava nerozbije existující funkcionalitu

### ✨ Nové funkce (Features)
- Přidávání nových kategorií emailů
- Vylepšení SMTP podpory
- Nové formáty exportu/importu

### 📚 Dokumentace
- Vylepšení README.md
- Přidání příkladů použití
- Překlady do dalších jazyků

### 🎨 UI/UX vylepšení
- Zlepšení uživatelského rozhraní
- Lepší error handling
- Informativnější logy

## 🛠️ Vývojové prostředí

### Požadavky
- **Python 3.6+**
- **Git**
- **Textový editor** (doporučeno VS Code, PyCharm)

### Testování
```bash
# Před odesláním PR otestujte:
python email_sender.py

# Zkontrolujte syntax:
python -m py_compile email_sender.py
```

### Struktura projektu
```
email_sender/
├── email_sender.py      # Hlavní skript
├── requirements.txt     # Python závislosti
├── .env.example        # Ukázkový konfigurační soubor
├── .gitignore          # Git ignore pravidla
├── README.md           # Dokumentace projektu
├── LICENSE             # MIT licence
└── CONTRIBUTING.md     # Tento soubor
```

## 🔍 Proces review

### Co očekávat
1. **Automatické kontroly**: Kontrola syntaxe a formátování
2. **Code review**: Manuální kontrola od maintainerů
3. **Testování**: Ověření funkcionality
4. **Merge**: Začlenění do main větve

### Timeline
- **Malé opravy**: 1-3 dny
- **Větší features**: 1-2 týdny
- **Breaking changes**: Vyžadují diskusi

## 📏 Coding Standards

### Python Style Guide
- Dodržujte **PEP 8** standardy
- Používejte **4 mezery** pro odsazení
- Maximální délka řádku: **88 znaků**
- Používejte **type hints** kde je to možné

### Příklad formátování:
```python
def send_email(subject: str, content: str, recipient: str) -> bool:
    """
    Odešle email s kompletním error handlingem.
    
    Args:
        subject: Předmět emailu
        content: Obsah emailu  
        recipient: Email příjemce
        
    Returns:
        True pokud byl email úspěšně odeslán, jinak False
    """
    try:
        # Implementace...
        return True
    except Exception as e:
        print(f"❌ Chyba: {e}")
        return False
```

### Commit Messages
Používejte **conventional commits** formát:
```
feat: přidání podpory pro Yahoo SMTP
fix: oprava validace email adresy
docs: aktualizace README s novými příklady
style: formátování kódu podle PEP 8
refactor: reorganizace email kategorií
test: přidání unit testů pro validaci
```

## 🐛 Hlášení chyb

### Před nahlášením
1. ✅ Zkontrolujte [existující issues](https://github.com/jirpo9/email_sender/issues)
2. ✅ Ověřte, že používáte nejnovější verzi
3. ✅ Zkuste reprodukovat chybu

### Informace k přiložení
- **OS a verze Pythonu**
- **Kroky k reprodukci**
- **Očekávaný výsledek**
- **Skutečný výsledek**
- **Error logy**
- **Konfigurace** (.env - bez hesel!)

### Template pro bug report
```markdown
**Popis chyby**
Stručný popis co se děje.

**Kroky k reprodukci**
1. Nastavte...
2. Spusťte...
3. Klikněte na...

**Očekávaný výsledek**
Co jste očekávali, že se stane.

**Skutečný výsledek**
Co se skutečně stalo.

**Prostředí**
- OS: [např. Windows 10, Ubuntu 20.04]
- Python verze: [např. 3.9.5]
- Verze projektu: [např. v1.0.0]

**Dodatečné informace**
Error logy, screenshoty, atd.
```

## 💡 Návrhy vylepšení

### Feature requesty vítáme!
- **GUI rozhraní** pro snazší použití
- **Databázová podpora** pro ukládání šablon
- **Scheduling** - automatické odesílání
- **Statistiky** odeslaných emailů
- **Import/Export** vlastních kategorií

### Diskuse
Před implementací větších změn:
1. Otevřete **GitHub Discussion** nebo **Issue**
2. Popište váš nápad a jeho přínos
3. Diskutujte s komunitou
4. Implementujte po odsouhlasení

## 🆘 Potřebujete pomoc?

### Komunikační kanály
- **GitHub Issues**: Pro bug reporty a feature requesty
- **GitHub Discussions**: Pro obecné diskuse
- **Email**: Pro citlivé otázky (viz README)

### Užitečné zdroje
- [Python dokumentace](https://docs.python.org/3/)
- [Git příručka](https://git-scm.com/doc)
- [GitHub příručka](https://docs.github.com/)
- [PEP 8 Style Guide](https://pep8.org/)

## 🎉 Uznání

Všichni přispěvatelé budou uvedeni v:
- **README.md** - v sekci Contributors
- **CHANGELOG.md** - při vydání nových verzí
- **GitHub Contributors** - automaticky

---

**Děkujeme za váš čas a úsilí! Vaše příspěvky pomáhají zlepšovat projekt pro celou komunitu. 🚀**
