import smtplib
import random
import time
import os 
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
from dotenv import load_dotenv



# Load .env file
load_dotenv()

# SMTP Configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))

# Get configuration from .env file
SENDER_EMAIL = os.getenv('EMAIL_USER')
SENDER_PASSWORD = os.getenv('EMAIL_PASS')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')

# Check that we have all required data
if not all([SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL]):
    print("❌ Missing required data in .env file!")
    print("Make sure .env file contains:")
    print("EMAIL_USER=your_email@gmail.com")
    print("EMAIL_PASS=your_app_password")
    print("RECIPIENT_EMAIL=target_email@domain.com")
    sys.exit(1)

# Basic email format validation
def validate_email(email):
    """Basic email address validation"""
    return "@" in email and "." in email.split("@")[1]

if not all(validate_email(email) for email in [SENDER_EMAIL, RECIPIENT_EMAIL]):
    raise ValueError("❌ Invalid email address format")

# Test SMTP connection before sending emails
def test_smtp_connection():
    """Test SMTP connection and authentication"""
    try:
        print("🔍 Testing SMTP connection...")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.set_debuglevel(0)  # Disable debug output for cleaner logs
            server.starttls()
            print("✅ TLS connection established")
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            print("✅ Authentication successful")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("💡 Solutions:")
        print("   1. Make sure you're using an App Password, not your regular Gmail password")
        print("   2. Generate a new App Password in Google Account Settings")
        print("   3. Ensure 2-Factor Authentication is enabled")
        return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False
    







# Company names for more realistic emails
COMPANY_NAMES = [
    "ABC s.r.o.", "XYZ a.s.", "Novák & Partners s.r.o.", "Stavební firma Dvořák s.r.o.",
    "IT Solutions Czech s.r.o.", "Gastro Praha s.r.o.", "Výroba a distribuce s.r.o.",
    "Služby Plus a.s.", "Obchodní dům Centrum s.r.o.", "Logistika CZ s.r.o."
]

# Sender names for variety
SENDER_NAMES = [
    "Jan Novák", "Petra Svobodová", "Martin Dvořák", "Eva Černá", "Tomáš Procházka",
    "Tereza Krejčová", "Pavel Marek", "Lucie Pokorná", "Jiří Veselý", "Anna Marková"
]

# Realistic email signatures
SIGNATURES = [
    "\n\nS pozdravem,\n{name}\n{company}\nTel: +420 {phone}\nEmail: {email}",
    "\n\nDěkuji a přeji hezký den,\n{name}\n{position}\n{company}",
    "\n\nS přátelským pozdravem,\n{name}\n{company}\n{phone}",
    "\n\n{name}\n{position}\n{company}\nMobil: +420 {phone}",
    "\n\nDěkuji za spolupráci.\n\n{name}\n{company}"
]





CATEGORIES = {
    "Mzdy": {
        "subjects": [
            "Výplatní pásky za {month} {year}",
            "Mzdové podklady - {company}",
            "Dotaz k výpočtu mezd",
            "Sociální a zdravotní odvody {month}/{year}",
            "Podklady pro mzdy - nový zaměstnanec",
            "Změna mzdových tarifů od {month}",
            "Roční zúčtování daně",
            "Nemocenská - {name}",
            "DPČ/DPP smlouvy k zaúčtování",
            "Přehled přesčasů za {month}"
        ],
        "contents": [
            """Dobrý den,

v příloze zasílám podklady pro zpracování mezd za {month} {year}. 

Změny oproti minulému měsíci:
- {name} - ukončení pracovního poměru k {date}
- Nový zaměstnanec od {date2} - podklady v příloze
- Změna úvazku u {name2} na 0.8 od příštího měsíce

Prosím o zpracování do {deadline}. Výplatní termín je standardně {date3}.

Pokud budete potřebovat další informace, jsem k dispozici.""",
            
            """Dobrý den,

zasílám docházku za {month} {year} ke zpracování mezd:

Celkem odpracováno: {hours} hodin
Dovolená: {vacation} dnů
Nemocenská: {sick} dnů ({name})
Přesčasy: {overtime} hodin

Příplatky:
- Noční směny: {night} hodin
- Víkendy: {weekend} hodin
- Svátky: {holiday} hodin

Prosím o kontrolu a zpracování. V případě nejasností mě kontaktujte.""",

            """Vážená paní účetní,

řešíme situaci s výpočtem mezd za minulý měsíc. Zaměstnanec {name} upozornil na nesrovnalost v částce {amount} Kč.

Podle našich záznamů měl odpracováno:
- Řádná pracovní doba: {hours} hodin  
- Přesčasy: {overtime} hodin
- Celková hrubá mzda by měla být: {gross} Kč

Můžete prosím zkontrolovat výpočet? Možná došlo k chybě v zadání přesčasů.

Předem děkuji za vyřízení.""",

            """Dobrý den,

potřeboval bych vystavit potvrzení o příjmu pro zaměstnance:

Jméno: {name}
Období: {period}
Účel: {purpose}

Dále bych potřeboval průměrný výdělek za posledních 12 měsíců pro účely výpočtu podpory.

Je možné to připravit do {deadline}? Zaměstnanec to potřebuje na úřad.""",

            """Dobrý den,

od {date} nastupuje nový zaměstnanec:

Jméno: {name}
Pozice: {position}
Hrubá mzda: {salary} Kč
Pracovní úvazek: {contract}
Benefity: stravenky, příspěvek na dopravu

V příloze zasílám:
- Pracovní smlouvu
- Přihlášku k pojištění
- Prohlášení k dani
- Kontaktní údaje

Prosím o zařazení do systému a první výplatu v řádném termínu."""
        ]
    },



 "Daně": {
        "subjects": [
            "DPH přiznání za {month}/{year}",
            "Podklady pro daň z příjmů {year}",
            "Kontrolní hlášení - oprava",
            "Zálohy na daň - {quarter}. čtvrtletí",
            "Daňová optimalizace - konzultace",
            "Souhrnné hlášení EU",
            "Silniční daň - vozový park",
            "Daň z nemovitosti {year}",
            "Žádost o potvrzení bezdlužnosti",
            "Vratka DPH - {month}"
        ],
        "contents": [
            """Dobrý den,

posílám podklady pro DPH za {month}/{year}:

Přijaté faktury: {received} ks, celkem {amount1} Kč
Vydané faktury: {issued} ks, celkem {amount2} Kč

Odpočet DPH: {vat1} Kč
DPH na výstupu: {vat2} Kč

Prosím o kontrolu a podání přiznání. Všechny doklady jsou v příloze rozřazené podle data.

Upozorňuji na fakturu č. {invoice} - dodavatel není plátce DPH.""",

            """Vážená paní účetní,

připravuji podklady pro daňové přiznání za rok {year}. 

Můžete mi prosím sdělit, co všechno budete potřebovat? Zatím mám připraveno:
- Přehled příjmů a výdajů
- Faktury za energie a nájem
- Cestovní příkazy
- Doklady o darech

Je potřeba ještě něco dalšího? Kdy je termín pro odevzdání?

Rád bych také konzultoval možnosti daňové optimalizace pro příští rok.""",

            """Dobrý den,

při kontrole jsem zjistil chybu v kontrolním hlášení za {month}:

Sekce A.4: uvedena špatná částka {amount1} Kč
Správně má být: {amount2} Kč
DIČ dodavatele: {dic}

Prosím o podání následného kontrolního hlášení. Je to urgentní, protože hrozí pokuta.

Omlouvám se za komplikace, příště budu pozornější.""",

            """Dobrý den,

blíží se splatnost záloh na daň z příjmů za {quarter}. čtvrtletí.

Aktuální hospodářský výsledek: {profit} Kč
Základ daně (odhad): {base} Kč
Výše zálohy: {advance} Kč

Souhlasíte s touto částkou, nebo navrhujete úpravu? Minule jsme platili {last} Kč.

Prosím o vyjádření do {deadline}, abychom stihli platbu.""",

            """Vážená paní účetní,

v souvislosti s plánovanou investicí do {investment} bych rád konzultoval daňové dopady.

Předpokládaná částka: {amount} Kč
Způsob financování: {financing}
Plánovaný termín: {date}

Zajímá mě:
1. Možnost uplatnění odpočtů
2. Optimální způsob zaúčtování
3. Vliv na zálohy na daň

Kdy byste měla čas na schůzku? Ideálně příští týden."""
        ]
    },



"Faktury": {
        "subjects": [
            "Faktury k zaúčtování - {month}",
            "Urgence - fa č. {invoice}",
            "Dobropis k faktuře {invoice}",
            "Schválení faktury nad limit",
            "Reklamace faktury od {company}",
            "Zálohová faktura - {project}",
            "Faktury ke schválení",
            "Oprava faktury - špatné DIČ",
            "Seznam nezaplacených faktur",
            "Faktura v cizí měně - {currency}"
        ],
        "contents": [
            """Dobrý den,

v příloze posílám faktury k zaúčtování za {month}:

Celkem: {count} faktur
Celková částka: {total} Kč včetně DPH

Poznámky:
- Fa č. {invoice1} - jedná se o zálohu na {service}
- Fa č. {invoice2} - rozúčtovat na střediska 50/50
- Fa č. {invoice3} - investice, ne do nákladů

Prosím o zaúčtování a přípravu plateb. Splatnosti jsou vyznačené.""",

            """Dobrý den,

urgentně řešíme nezaplacenou fakturu:

Číslo faktury: {invoice}
Dodavatel: {company}
Částka: {amount} Kč
Splatnost: {duedate} (po splatnosti {days} dní)

Dodavatel hrozí zastavením dodávek. Můžete prosím prověřit, zda byla faktura zaplacena? Možná je chyba v čísle účtu nebo VS.

Děkuji za rychlé vyřízení.""",

            """Vážená paní účetní,

zasílám dobropis k faktuře č. {invoice}:

Původní částka: {original} Kč
Důvod dobropisu: {reason}
Nová částka: {new} Kč

V příloze je dobropis i původní faktura. Prosím o zaúčtování a úpravu v systému.

Pokud bude potřeba další dokumentace, dejte vědět.""",

            """Dobrý den,

potřebuji váš souhlas s proplacením faktury:

Dodavatel: {company}
Předmět: {subject}
Částka: {amount} Kč (překračuje limit {limit} Kč)

Jedná se o {description}. Nabídky od jiných dodavatelů byly výrazně dražší.

Prosím o schválení, abychom mohli pokračovat v projektu.""",

            """Dobrý den,

přišla nám faktura v {currency}:

Dodavatel: {company} ({country})
Částka: {amount} {currency}
Kurz ČNB k {date}: {rate}
Přepočet: {czk} Kč

Jak správně zaúčtovat? Použít kurz ČNB nebo kurz banky při platbě?

Děkuji za radu."""
        ]
    },


  "Rozpočet": {
        "subjects": [
            "Rozpočet na rok {year} - draft",
            "Čerpání rozpočtu {month}/{year}",
            "Překročení rozpočtu - {department}",
            "Úprava rozpočtu Q{quarter}",
            "Rozpočtová kontrola",
            "Investiční rozpočet {year}",
            "Úsporná opatření",
            "Rozpočet projektu {project}",
            "Cash flow - aktualizace",
            "Mimořádné výdaje - žádost"
        ],
        "contents": [
            """Dobrý den,

zasílám první návrh rozpočtu na rok {year}:

Plánované výnosy: {revenue} Kč
Plánované náklady: {costs} Kč
Očekávaný zisk: {profit} Kč

Hlavní předpoklady:
- Růst tržeb o {growth}%
- Inflace {inflation}%
- Nové investice: {investments} Kč

Prosím o připomínky do {deadline}. Příští týden bych rád svolal schůzku.""",

            """Vážená paní účetní,

posílám report čerpání rozpočtu za {month}:

Oddělení: {department}
Rozpočet: {budget} Kč
Čerpáno: {spent} Kč ({percentage}%)
Zbývá: {remaining} Kč

Hlavní položky:
- Mzdy: {salaries} Kč
- Materiál: {material} Kč
- Služby: {services} Kč

Jsme v limitu, ale v {month2} očekáváme vyšší náklady kvůli {reason}.""",

            """URGENTNÍ - Překročení rozpočtu

Dobrý den,

upozorňuji na překročení rozpočtu:

Středisko: {department}
Položka: {item}
Rozpočet: {budget} Kč
Skutečnost: {actual} Kč
Překročení: {over} Kč ({percentage}%)

Důvod: {reason}

Navrhuji následující opatření:
1. {measure1}
2. {measure2}

Prosím o váš názor a schválení dalšího postupu.""",

            """Dobrý den,

na základě výsledků za Q{quarter} navrhuji úpravu rozpočtu:

Původní rozpočet: {original} Kč
Navrhovaná úprava: {adjusted} Kč
Důvod: {reason}

Změny v položkách:
- Marketing: {marketing}
- IT: {it}
- Provoz: {operations}

Bez této úpravy nebudeme schopni {consequence}.

Kdy můžeme projednat?""",

            """Dobrý den,

žádám o schválení mimořádného výdaje:

Účel: {purpose}
Částka: {amount} Kč
Termín: {date}
Přínos: {benefit}

Tento výdaj není v rozpočtu, ale {justification}.

Možnosti financování:
1. Přesun z položky {item1}
2. Použití rezervy
3. Odložení {item2}

Prosím o rozhodnutí do {deadline}."""
        ]
    },


 "Pohledávky": {
        "subjects": [
            "Seznam dlužníků k {date}",
            "Upomínka - {company}",
            "Návrh na odpis pohledávky",
            "Právní vymáhání - {company}",
            "Splátkový kalendář - žádost",
            "Pohledávky po splatnosti",
            "Inventura pohledávek {year}",
            "Započtení pohledávek",
            "Postoupení pohledávky",
            "Analýza platební morálky"
        ],
        "contents": [
            """Dobrý den,

zasílám aktuální seznam pohledávek po splatnosti:

Celkem: {total} Kč
Počet dlužníků: {count}

TOP 5 dlužníků:
1. {company1} - {amount1} Kč ({days1} dní po splatnosti)
2. {company2} - {amount2} Kč ({days2} dní po splatnosti)
3. {company3} - {amount3} Kč ({days3} dní po splatnosti)
4. {company4} - {amount4} Kč ({days4} dní po splatnosti)
5. {company5} - {amount5} Kč ({days5} dní po splatnosti)

Doporučuji zahájit vymáhání u pohledávek nad 60 dní.""",

            """UPOMÍNKA č. 3 - POSLEDNÍ PŘED PRÁVNÍM VYMÁHÁNÍM

Vážený zákazníku,

upozorňujeme Vás na neuhrazenou pohledávku:

Faktura č.: {invoice}
Částka: {amount} Kč
Splatnost: {duedate}
Dní po splatnosti: {days}

Přes opakované upomínky jste závazek neuhradili. Pokud neobdržíme platbu do {deadline}, budeme nuceni předat pohledávku právnímu oddělení.

S pozdravem""",

            """Dobrý den,

navrhuji odepsat následující pohledávku:

Dlužník: {company}
Částka: {amount} Kč
Stáří: {age} měsíců
Důvod: {reason}

Vymáhání je neekonomické, protože:
- Dlužník je v insolvenci
- Náklady na vymáhání by přesáhly hodnotu pohledávky
- Pohledávka je promlčená

Prosím o schválení odpisu a zaúčtování.""",

            """Dobrý den,

klient {company} žádá o splátkový kalendář:

Dlužná částka: {amount} Kč
Navrhované splátky: {installment} Kč měsíčně
Doba splácení: {months} měsíců
První splátka: {date}

Klient má dlouhodobě dobrou platební morálku, současné problémy jsou způsobeny {reason}.

Doporučuji schválit s podmínkou:
- Úrok z prodlení {interest}%
- Okamžitá splatnost při nedodržení splátek

Souhlasíte?""",

            """Dobrý den,

pro inventuru potřebuji odsouhlasit pohledávky:

Celkový stav k {date}: {total} Kč

Struktura:
- Do splatnosti: {current} Kč
- Po splatnosti 0-30 dní: {overdue30} Kč
- Po splatnosti 31-90 dní: {overdue90} Kč
- Po splatnosti nad 90 dní: {overdue90plus} Kč

Prosím o kontrolu a potvrzení správnosti. Případné rozdíly musíme vyřešit do konce měsíce."""
        ]
    },


 "Inventura": {
        "subjects": [
            "Zahájení inventury {year}",
            "Inventurní rozdíly - sklad",
            "Protokol o inventuře",
            "Inventura majetku - IT",
            "Mimořádná inventura",
            "Inventurní soupisy k podpisu",
            "Vyřazení majetku",
            "Přecenění zásob",
            "Inventura pokladny",
            "Závěrečná zpráva inventury"
        ],
        "contents": [
            """Dobrý den,

zahajujeme roční inventuru majetku a závazků k {date}.

Harmonogram:
- {date1}: Inventura skladů
- {date2}: Inventura majetku
- {date3}: Inventura pohledávek a závazků
- {date4}: Inventura pokladen

Inventurní komise:
Předseda: {name1}
Členové: {name2}, {name3}

Prosím o přípravu podkladů a součinnost. Případné inventurní rozdíly řešte ihned se mnou.""",

            """Dobrý den,

při inventuře skladu byly zjištěny rozdíly:

Manka:
- {item1}: {quantity1} ks (hodnota {value1} Kč)
- {item2}: {quantity2} ks (hodnota {value2} Kč)

Přebytky:
- {item3}: {quantity3} ks (hodnota {value3} Kč)

Celkový rozdíl: {difference} Kč

Pravděpodobná příčina: {reason}

Navrhuji: {action}. Prosím o vyjádření a schválení zaúčtování.""",

            """Vážená paní účetní,

zasílám protokol o provedené inventuře:

Druh inventury: {type}
Datum provedení: {date}
Inventarizovaný majetek: {assets}

Zjištěný stav:
- Účetní evidence: {book} Kč
- Skutečný stav: {actual} Kč
- Rozdíl: {difference} Kč

Závěr: {conclusion}

Protokol je v příloze k podpisu. Prosím o zaúčtování případných rozdílů.""",

            """Dobrý den,

na základě inventury navrhuji vyřadit následující majetek:

1. {asset1} - inv.č. {number1}, PC {value1} Kč (důvod: {reason1})
2. {asset2} - inv.č. {number2}, PC {value2} Kč (důvod: {reason2})
3. {asset3} - inv.č. {number3}, PC {value3} Kč (důvod: {reason3})

Celková zůstatková hodnota: {total} Kč

Majetek je již nefunkční a oprava je neekonomická. Prosím o schválení vyřazení a likvidaci.""",

            """Dobrý den,

dokončili jsme inventuru zásob. Je potřeba přecenění:

Materiál {material}:
- Účetní cena: {bookprice} Kč/ks
- Tržní cena: {marketprice} Kč/ks
- Množství: {quantity} ks
- Dopad: {impact} Kč

Důvod poklesu ceny: {reason}

Prosím o zaúčtování opravné položky. Dokumentace v příloze."""
        ]
    },


"Dotace": {
        "subjects": [
            "Dotační výzva - {program}",
            "Vyúčtování dotace {project}",
            "Žádost o platbu - milestone {number}",
            "Kontrola dotace - příprava",
            "Změna v projektu - oznámení",
            "Dotace - vrácení části",
            "Monitorovací zpráva",
            "Udržitelnost projektu",
            "Nová dotační příležitost",
            "Konzultace k dotaci"],
        "contents": [
            """Dobrý den,

objevila se nová dotační výzva:

Program: {program}
Poskytovatel: {provider}
Max. výše dotace: {amount} Kč
Míra podpory: {percentage}%
Termín podání: {deadline}

Podporované aktivity:
- {activity1}
- {activity2}
- {activity3}

Myslím, že bychom mohli žádat na {purpose}. Předpokládané náklady {costs} Kč.

Máte zkušenosti s tímto programem? Pomůžete s přípravou?""",

            """Dobrý den,

připravuji vyúčtování dotace:

Projekt: {project}
Číslo: {number}
Období: {period}
Čerpáno: {spent} Kč z {total} Kč

Potřebuji od vás:
- Soupis účetních dokladů
- Kopie faktur
- Výpisy z účtu
- Mzdové listy

Termín odevzdání: {deadline}

Můžete mi to připravit do {date}? Kontrola bude přísná.""",

            """URGENTNÍ - Kontrola dotace

Dobrý den,

byli jsme vybrání ke kontrole projektu {project}.

Termín kontroly: {date}
Kontrolní orgán: {authority}

Budou kontrolovat:
- Účetní doklady
- Veřejné zakázky
- Publicitu
- Naplnění indikátorů

Prosím o přípravu všech podkladů. Sejděme se {meeting} na přípravu.""",

            """Dobrý den,

musíme řešit problém s dotací:

Projekt: {project}
Problém: {problem}
Dopad: možnost krácení o {amount} Kč

Navrhuji řešení:
1. {solution1}
2. {solution2}

Je nutné podat žádost o změnu do {deadline}. Prosím o váš názor a pomoc s formulací.""",

            """Dobrý den,

blíží se konec udržitelnosti projektu {project}.

Povinnosti:
- Zachovat {indicator1} po dobu {period}
- Reportovat {indicator2} každý rok
- Archivovat dokumenty do {year}

Aktuální stav:
{status}

Prosím o evidenci a sledování. Při nedodržení hrozí vrácení dotace {amount} Kč."""
        ]
    },
    
    "Audit": {
        "subjects": [
            "Audit {year} - zahájení",
            "Požadavky auditora - doplnění",
            "Management letter",
            "Předauditní příprava",
            "Auditní zjištění - vyjádření",
            "Výrok auditora",
            "Interní audit procesů",
            "Audit dotací",
            "Daňový audit - oznámení",
            "Nápravná opatření - plnění"
        ],
        "contents": [
            """Dobrý den,

informuji o zahájení auditu účetní závěrky za rok {year}.

Auditor: {auditor}
Termín: {date1} - {date2}
Rozsah: {scope}

Požadované podklady:
- Účetní závěrka
- Hlavní kniha
- Inventurní soupisy
- Smlouvy nad {amount} Kč
- Bankovní konfirmace

Prosím o přípravu do {deadline}. První schůzka {meeting}.""",

            """Dobrý den,

auditor požaduje doplnění:

1. Detailní rozpis položky {item} ({amount} Kč)
2. Smlouvy k pohledávce za {company}
3. Dokumentaci k odpisu {asset}
4. Výpočet rezervy na {provision}

Termín: do {deadline}

Můžete prosím připravit? Některé věci možná budeme muset vysvětlit osobně.""",

            """Vážená paní účetní,

auditor zaslal předběžná zjištění:

Zjištění č. 1: {finding1}
Dopad: {impact1}
Doporučení: {recommendation1}

Zjištění č. 2: {finding2}
Dopad: {impact2}
Doporučení: {recommendation2}

Prosím o váš komentář do {deadline}. Některá zjištění můžeme rozporovat.""",

            """Dobrý den,

přišel finální výrok auditora:

Výrok: {opinion}
Datum: {date}

Hlavní připomínky:
{comments}

Celkově hodnotí účetnictví jako {evaluation}. Musíme implementovat doporučení do {deadline}.

Gratuluji k úspěšnému auditu!""",

            """Dobrý den,

daňový úřad oznámil kontrolu:

Předmět: {subject}
Období: {period}
Zahájení: {date}
Kontrolor: {inspector}

Budou požadovat:
- {document1}
- {document2}
- {document3}

Máme právo na přípravu {days} dní. Doporučuji konzultaci s daňovým poradcem."""
        ]
    },
    
    "Výkazy": {
        "subjects": [
            "Účetní závěrka {year}",
            "Měsíční reporting {month}",
            "Výkazy pro banku",
            "Konsolidační balíček",
            "Statistické výkazy",
            "Cash flow statement",
            "Zkrácená rozvaha k {date}",
            "Mezitímní závěrka",
            "Výkazy pro mateřskou společnost",
            "Oprava výkazů - {period}"
        ],
        "contents": [
            """Dobrý den,

připravuji účetní závěrku za rok {year}:

Aktiva celkem: {assets} Kč
Pasiva celkem: {liabilities} Kč
Výnosy: {revenue} Kč
Náklady: {costs} Kč
HV před zdaněním: {profit} Kč

Prosím o kontrolu hlavních položek:
- Odpisy: {depreciation} Kč
- Rezervy: {provisions} Kč
- Opravné položky: {adjustments} Kč

Termín odevzdání: {deadline}""",

            """Dobrý den,

zasílám měsíční výkazy za {month}:

Tržby: {revenue} Kč ({percentage1}% vs. plán)
EBITDA: {ebitda} Kč ({percentage2}% vs. LY)
Čistý zisk: {profit} Kč

KPIs:
- Obrat/zaměstnanec: {kpi1} Kč
- Marže: {kpi2}%
- ROE: {kpi3}%

Komentář: {comment}

Detaily v příloze.""",

            """Dobrý den,

banka požaduje čtvrtletní výkazy:

Požadované dokumenty:
- Rozvaha
- Výsledovka
- Cash flow
- Analýza pohledávek
- Plnění covenantů

Speciální požadavek: {requirement}

Termín: {deadline}

Můžete připravit? Potřebují to pro {purpose}.""",

            """Dobrý den,

při kontrole výkazů jsem našel chybu:

Výkaz: {statement}
Období: {period}
Řádek: {line}
Chybná hodnota: {wrong} Kč
Správná hodnota: {correct} Kč

Dopad: {impact}

Prosím o opravu a znovu odeslání. Pokud byly výkazy již odeslány {recipient}, musíme informovat.""",

            """Dobrý den,

mateřská společnost požaduje konsolidační balíček:

Termín: {deadline}
Formát: {format}
Měna: {currency}

Speciální požadavky:
- Mezipodnikové transakce
- Transfer pricing dokumentace
- Sesouhlasení IC zůstatků

První draft pošlu {date}. Budete mít čas na kontrolu?"""
        ]
    },
    
    "Bankovnictví": {
        "subjects": [
            "Bankovní výpisy - nesrovnalost",
            "Nový bankovní účet - info",
            "Poplatky {month}/{year}",
            "Kontokorent - čerpání",
            "Bankovní garance",
            "SEPA inkaso - souhlas",
            "Platba do zahraničí",
            "Změna podpisových vzorů",
            "Termínovaný vklad",
            "Bankovní konfirmace"
        ],
        "contents": [
            """Dobrý den,

při kontrole bankovních výpisů jsem našel nesrovnalost:

Účet: {account}
Datum: {date}
Částka dle výpisu: {bank} Kč
Částka dle účetnictví: {books} Kč
Rozdíl: {difference} Kč

Může se jednat o:
- Nezaúčtovanou platbu
- Bankovní poplatek
- Kurzový rozdíl

Můžete prosím prověřit?""",

            """Dobrý den,

informuji o založení nového účtu:

Banka: {bank}
Číslo účtu: {account}
Měna: {currency}
Účel: {purpose}

Podpisová práva: {signatories}

Prosím o:
- Zavedení do účetního systému
- Nastavení v internetovém bankovnictví
- Aktualizaci seznamu účtů

Výpisy budou chodit {frequency}.""",

            """Dobrý den,

řešíme vysoké bankovní poplatky:

Měsíc: {month}
Celkem: {total} Kč

Největší položky:
- Vedení účtu: {fee1} Kč
- Platby: {fee2} Kč
- Výpisy: {fee3} Kč
- Ostatní: {fee4} Kč

Navrhuji:
1. Jednání s bankou o slevě
2. Změna tarifu
3. Konsolidace účtů

Co myslíte?""",

            """Dobrý den,

potřebujeme zajistit platbu do zahraničí:

Příjemce: {beneficiary}
Země: {country}
Částka: {amount} {currency}
Účel: {purpose}
Termín: {date}

Dokumenty:
- Faktura č. {invoice}
- Smlouva

Prosím o přípravu platebního příkazu. Nezapomeňte na správný BIC/SWIFT.""",

            """Dobrý den,

banka požaduje roční konfirmaci zůstatků:

K datu: {date}
Účty: {accounts}

Potřebují:
- Potvrzení zůstatků
- Seznam oprávněných osob
- Aktuální podpisové vzory

Termín: {deadline}

Můžete prosím vyřídit? Je to pro audit."""
        ]
    }
}
    









def generate_random_values():
    """Generate random realistic values for email templates"""
    months = ["leden", "únor", "březen", "duben", "květen", "červen", 
              "červenec", "srpen", "září", "říjen", "listopad", "prosinec"]
    
    current_year = datetime.now().year
    years = [str(current_year - 1), str(current_year), str(current_year + 1)]
    
    # Generate random dates
    today = datetime.now()
    date1 = today - timedelta(days=random.randint(1, 30))
    date2 = today + timedelta(days=random.randint(1, 30))
    date3 = today + timedelta(days=random.randint(5, 15))
    date4 = today + timedelta(days=random.randint(20, 40))
    
    # Random values for templates
    values = {
        # Basic values
        "month": random.choice(months),
        "month2": random.choice(months),
        "year": random.choice(years),
        "quarter": random.randint(1, 4),
        "date": date1.strftime("%d.%m.%Y"),
        "date1": date1.strftime("%d.%m.%Y"),
        "date2": date2.strftime("%d.%m.%Y"),
        "date3": date3.strftime("%d.%m.%Y"),
        "date4": date4.strftime("%d.%m.%Y"),
        "deadline": date3.strftime("%d.%m.%Y"),
        "duedate": date2.strftime("%d.%m.%Y"),
        "meeting": f"{date2.strftime('%d.%m.')} v 14:00",
        
        # Company and person names
        "company": random.choice(COMPANY_NAMES),
        "company1": random.choice(COMPANY_NAMES),
        "company2": random.choice(COMPANY_NAMES),
        "company3": random.choice(COMPANY_NAMES),
        "company4": random.choice(COMPANY_NAMES),
        "company5": random.choice(COMPANY_NAMES),
        "name": random.choice(SENDER_NAMES),
        "name1": random.choice(SENDER_NAMES),
        "name2": random.choice(SENDER_NAMES),
        "name3": random.choice(SENDER_NAMES),
        
        # Numbers and amounts
        "number": f"{random.randint(100000, 999999)}",
        "invoice": f"FV{current_year}{random.randint(1000, 9999)}",
        "invoice1": f"FV{current_year}{random.randint(1000, 9999)}",
        "invoice2": f"FV{current_year}{random.randint(1000, 9999)}",
        "invoice3": f"FV{current_year}{random.randint(1000, 9999)}",
        "amount": f"{random.randint(10, 500) * 1000:,}".replace(",", " "),
        "amount1": f"{random.randint(10, 500) * 1000:,}".replace(",", " "),
        "amount2": f"{random.randint(10, 500) * 1000:,}".replace(",", " "),
        "gross": f"{random.randint(30, 80) * 1000:,}".replace(",", " "),
        "total": f"{random.randint(100, 5000) * 1000:,}".replace(",", " "),
        "czk": f"{random.randint(10, 500) * 1000:,}".replace(",", " "),
        
        # Percentages and rates
        "percentage": random.randint(60, 120),
        "percentage1": random.randint(80, 120),
        "percentage2": random.randint(90, 110),
        "growth": random.randint(3, 15),
        "inflation": round(random.uniform(2.5, 5.5), 1),
        "interest": round(random.uniform(5.0, 8.5), 1),
        "rate": round(random.uniform(24.5, 26.5), 3),
        
        # Work related
        "hours": random.randint(140, 180),
        "overtime": random.randint(0, 30),
        "vacation": random.randint(0, 10),
        "sick": random.randint(0, 5),
        "night": random.randint(0, 40),
        "weekend": random.randint(0, 20),
        "holiday": random.randint(0, 16),
        "days": random.randint(5, 90),
        "days1": random.randint(30, 180),
        "days2": random.randint(15, 90),
        "days3": random.randint(7, 60),
        "days4": random.randint(20, 120),
        "days5": random.randint(10, 75),
        
        # Financial values
        "salary": f"{random.randint(25, 80) * 1000:,}".replace(",", " "),
        "revenue": f"{random.randint(1000, 50000) * 1000:,}".replace(",", " "),
        "costs": f"{random.randint(800, 40000) * 1000:,}".replace(",", " "),
        "profit": f"{random.randint(100, 10000) * 1000:,}".replace(",", " "),
        "budget": f"{random.randint(100, 5000) * 1000:,}".replace(",", " "),
        "spent": f"{random.randint(50, 4000) * 1000:,}".replace(",", " "),
        "remaining": f"{random.randint(10, 1000) * 1000:,}".replace(",", " "),
        "actual": f"{random.randint(100, 6000) * 1000:,}".replace(",", " "),
        "salaries": f"{random.randint(500, 10000) * 1000:,}".replace(",", " "),
        "services": f"{random.randint(50, 2000) * 1000:,}".replace(",", " "),
        "investments": f"{random.randint(500, 10000) * 1000:,}".replace(",", " "),
        
        # Other specific values
        "position": random.choice(["účetní", "ekonom", "finanční manažer", "controller", "mzdová účetní"]),
        "contract": random.choice(["plný úvazek", "0.8 úvazku", "0.5 úvazku", "DPP", "DPČ"]),
        "currency": random.choice(["EUR", "USD", "GBP"]),
        "country": random.choice(["Německo", "Rakousko", "Polsko", "Slovensko"]),
        "purpose": random.choice(["hypotéka", "úvěr", "žádost o dotaci", "výběrové řízení", "hodnocení bonity"]),
        "project": random.choice(["Modernizace IT", "Nová výrobní linka", "Expanze", "ERP systém"]),
        "department": random.choice(["Výroba", "Obchod", "Marketing", "IT", "Správa"]),
        "period": f"{random.choice(months)} - {random.choice(months)} {random.choice(years)}",
        "recipient": random.choice(["ČSÚ", "finanční úřad", "ČSSZ", "zdravotní pojišťovna", "banka"]),
        
        # Additional specific values for templates
        "phone": f"{random.randint(600, 799)} {random.randint(100, 999)} {random.randint(100, 999)}",
        "email": f"{random.choice(['info', 'ucetni', 'fakturace', 'ekonom'])}@example.cz",
        "dic": f"CZ{random.randint(10000000, 99999999)}",
        "account": f"{random.randint(1000000000, 9999999999)}/{random.choice(['0100', '0300', '0600', '0800'])}",
        "count": random.randint(5, 50),
        "received": random.randint(10, 100),
        "issued": random.randint(5, 50),
        "vat1": f"{random.randint(10, 500) * 1000:,}".replace(",", " "),
        "vat2": f"{random.randint(15, 600) * 1000:,}".replace(",", " "),
        "action": random.choice(["zaúčtování jako manko", "prošetření příčin", "inventura celého skladu"]),
    }
    
    # Add more specific random values based on context
    values.update({
        "base": f"{random.randint(500, 5000) * 1000:,}".replace(",", " "),
        "advance": f"{random.randint(50, 500) * 1000:,}".replace(",", " "),
        "last": f"{random.randint(45, 450) * 1000:,}".replace(",", " "),
        "limit": f"{random.randint(50, 200) * 1000:,}".replace(",", " "),
        "original": f"{random.randint(100, 1000) * 1000:,}".replace(",", " "),
        "new": f"{random.randint(80, 800) * 1000:,}".replace(",", " "),
        "adjusted": f"{random.randint(120, 1200) * 1000:,}".replace(",", " "),
        "investment": random.choice(["nové stroje", "software", "vozový park", "budova", "technologie"]),
        "financing": random.choice(["vlastní zdroje", "bankovní úvěr", "leasing", "dotace"]),
        "service": random.choice(["IT služby", "poradenství", "školení", "údržba", "marketing"]),
        "reason": random.choice(["nečekaný výpadek", "změna legislativy", "nový projekt", "rozšíření týmu", "chyba v evidenci"]),
        "description": random.choice(["specializované zařízení", "software licence", "odborné služby"]),
        "subject": random.choice(["Nákup kancelářských potřeb", "IT vybavení", "Služby externího poradce", "Marketingová kampaň"]),
        
        # Audit specific values
        "auditor": random.choice(["PwC", "Deloitte", "EY", "KPMG", "BDO", "Mazars"]),
        "scope": random.choice(["kompletní audit", "statutární audit", "audit dotací", "částečný audit"]),
        "item": random.choice(["Rezervy", "Odpisy", "Zásoby", "Pohledávky", "Dlouhodobý majetek"]),
        "asset": random.choice(["stroj XY", "software", "budova", "vozidlo", "licence"]),
        "provision": random.choice(["dovolenou", "bonusy", "záruční opravy", "soudní spory"]),
        "finding1": "Nesprávné ocenění zásob",
        "finding2": "Chybějící dokumentace k některým výdajům",
        "impact1": "Možné nadhodnocení aktiv",
        "impact2": "Nedostatečná průkaznost nákladů",
        "recommendation1": "Přecenit zásoby dle aktuálních cen",
        "recommendation2": "Doplnit chybějící doklady",
        "opinion": random.choice(["Bez výhrad", "S výhradou", "Odmítnutí výroku"]),
        "comments": "Účetnictví je vedeno v souladu s předpisy, drobné nedostatky v dokumentaci",
        "evaluation": random.choice(["velmi dobré", "dobré", "vyhovující", "s výhradami"]),
        "inspector": random.choice(["Ing. Novák", "Mgr. Dvořáková", "Ing. Procházka", "JUDr. Svoboda"]),
        "document1": "Hlavní kniha",
        "document2": "Faktury nad 100 000 Kč",
        "document3": "Bankovní výpisy",
        
        # Additional values for other templates
        "assets": f"{random.randint(10000, 500000) * 1000:,}".replace(",", " "),
        "liabilities": f"{random.randint(10000, 500000) * 1000:,}".replace(",", " "),
        "depreciation": f"{random.randint(100, 5000) * 1000:,}".replace(",", " "),
        "provisions": f"{random.randint(50, 2000) * 1000:,}".replace(",", " "),
        "adjustments": f"{random.randint(10, 1000) * 1000:,}".replace(",", " "),
        "ebitda": f"{random.randint(500, 20000) * 1000:,}".replace(",", " "),
        "kpi1": f"{random.randint(500, 2000) * 1000:,}".replace(",", " "),
        "kpi2": f"{random.randint(5, 30)}",
        "kpi3": f"{random.randint(5, 25)}",
        "comment": "Výsledky jsou v souladu s plánem",
        "requirement": "Detailní analýza cash flow",
        "statement": random.choice(["Rozvaha", "Výsledovka", "Cash flow"]),
        "line": f"ř. {random.randint(10, 200)}",
        "wrong": f"{random.randint(100, 5000) * 1000:,}".replace(",", " "),
        "correct": f"{random.randint(100, 5000) * 1000:,}".replace(",", " "),
        "impact": "Změna hospodářského výsledku",
        "format": random.choice(["Excel", "PDF", "XML", "XBRL"]),
        "bank": random.choice(["Česká spořitelna", "ČSOB", "Komerční banka", "UniCredit", "Raiffeisenbank"]),
        "books": f"{random.randint(1000, 50000) * 1000:,}".replace(",", " "),
        "book": f"{random.randint(1000, 50000) * 1000:,}".replace(",", " "),
        "difference": f"{random.randint(1, 1000) * 1000:,}".replace(",", " "),
        "signatories": "dva podpisy společně",
        "frequency": random.choice(["denně", "týdně", "měsíčně"]),
        "fee1": f"{random.randint(200, 2000)}",
        "fee2": f"{random.randint(100, 1000)}",
        "fee3": f"{random.randint(50, 500)}",
        "fee4": f"{random.randint(100, 1000)}",
        "beneficiary": "Company Ltd.",
        "accounts": "všechny CZK účty",
        
        # More specific values
        "current": f"{random.randint(1000, 10000) * 1000:,}".replace(",", " "),
        "overdue30": f"{random.randint(500, 5000) * 1000:,}".replace(",", " "),
        "overdue90": f"{random.randint(200, 2000) * 1000:,}".replace(",", " "),
        "overdue90plus": f"{random.randint(100, 1000) * 1000:,}".replace(",", " "),
        "installment": f"{random.randint(10, 100) * 1000:,}".replace(",", " "),
        "months": random.randint(6, 24),
        "age": random.randint(12, 36),
        "quantity1": random.randint(1, 100),
        "quantity2": random.randint(1, 50),
        "quantity3": random.randint(1, 30),
        "quantity": random.randint(100, 1000),
        "value1": f"{random.randint(1, 100) * 1000:,}".replace(",", " "),
        "value2": f"{random.randint(1, 50) * 1000:,}".replace(",", " "),
        "value3": f"{random.randint(1, 30) * 1000:,}".replace(",", " "),
        "item1": random.choice(["Marketing", "Cestovné", "Školení", "Reprezentace", "kancelářské potřeby"]),
        "item2": random.choice(["nákup IT", "renovace kanceláří", "nový projekt"]),
        "item3": "Materiál XY",
        "type": random.choice(["řádná", "mimořádná", "průběžná"]),
        "conclusion": "Skutečný stav odpovídá účetní evidenci",
        "asset1": "Notebook HP",
        "asset2": "Tiskárna Canon",
        "asset3": "Nábytek kancelář 205",
        "number1": f"DHM{random.randint(1000, 9999)}",
        "number2": f"DHM{random.randint(1000, 9999)}",
        "number3": f"DNM{random.randint(100, 999)}",
        "reason1": "nefunkční, neopravitelné",
        "reason2": "zastaralé, bez podpory",
        "reason3": "poškozené, náhrada",
        "material": random.choice(["Ocelové profily", "Kancelářský papír", "Elektronické součástky"]),
        "bookprice": f"{random.randint(100, 500)}",
        "marketprice": f"{random.randint(80, 400)}",
        "program": random.choice(["OP PIK", "OP TAK", "IROP", "Antivirus", "COVID Plus"]),
        "provider": random.choice(["MPO", "MPSV", "MMR", "MŽP", "TAČR"]),
        "activity1": "Nákup technologií",
        "activity2": "Vzdělávání zaměstnanců",
        "activity3": "Výzkum a vývoj",
        "problem": "Nedočerpání plánované částky",
        "solution1": "Žádost o změnu rozpočtu",
        "solution2": "Přesun mezi kapitolami",
        "indicator1": f"{random.randint(5, 20)} pracovních míst",
        "indicator2": "obrat",
        "status": "Všechny indikátory plněny",
        "authority": random.choice(["CRR", "SFŽP", "ROP", "Finanční úřad"]),
        "over": f"{random.randint(10, 100) * 1000:,}".replace(",", " "),
        "measure1": "Omezení nákupů do konce roku",
        "measure2": "Přesun prostředků z jiné kapitoly",
        "marketing": "+20%",
        "it": "-10%",
        "operations": "beze změny",
        "consequence": "dokončit klíčový projekt",
        "justification": "jedná se o jedinečnou příležitost",
        "benefit": "úspora 30% nákladů ročně",
    })
    
    return values

def create_realistic_signature(values):
    """Create a realistic email signature"""
    signature_template = random.choice(SIGNATURES)
    
    sig_values = {
        "name": values.get("name", random.choice(SENDER_NAMES)),
        "company": values.get("company", random.choice(COMPANY_NAMES)),
        "position": values.get("position", "účetní"),
        "phone": f"+420 {values.get('phone', '777 123 456')}",
        "email": values.get("email", "ucetni@firma.cz")
    }
    
    try:
        return signature_template.format(**sig_values)
    except:
        return f"\n\nS pozdravem,\n{sig_values['name']}\n{sig_values['company']}"

def send_email(subject, content, recipient):
    """Send one email with complete error handling"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = f"{random.choice(SENDER_NAMES)} <{SENDER_EMAIL}>"
        msg['To'] = recipient
        msg['Subject'] = subject
        msg['Date'] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0100")
        
        # Sometimes add Reply-To header for realism
        if random.random() > 0.7:
            msg['Reply-To'] = SENDER_EMAIL
        
        # Add content
        msg.attach(MIMEText(content, 'plain', 'utf-8'))
        
        # Sometimes add a "fake" attachment reference in the email
        if random.random() > 0.6:
            content += "\n\nPřílohy: dokument.pdf"
        
        # Connect to SMTP server and send
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        
        return True
        
    except Exception as e:
        print(f"❌ Error while sending: {e}")
        return False

def send_test_email():
    """Send a single test email first"""
    print("📧 Sending test email...")
    subject = "Test email - Accounting Email Generator"
    content = f"""Dobrý den,

toto je testovací email pro ověření konfigurace.

Čas odeslání: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}

Pokud tento email vidíte, konfigurace funguje správně.

S pozdravem,
Testovací systém"""
    
    return send_email(subject, content, RECIPIENT_EMAIL)

def main():
    """Main function - send 50 emails (5 for each category)"""
    print("🔧 CONFIGURATION CHECK:")
    print(f"📧 Sender email: {SENDER_EMAIL}")
    print(f"📥 Recipient email: {RECIPIENT_EMAIL}")
    print(f"🔗 SMTP server: {SMTP_SERVER}:{SMTP_PORT}")
    
    # Test SMTP connection first
    if not test_smtp_connection():
        print("\n❌ SMTP connection test failed. Please fix authentication issues before continuing.")
        return
    
    # Send test email first
    print("\n🧪 Sending test email first...")
    if not send_test_email():
        print("❌ Test email failed. Stopping.")
        return
    else:
        print("✅ Test email sent successfully!")
    
    print("\n🚀 Starting to send accounting test emails...")
    print(f"📊 Number of categories: {len(CATEGORIES)}")
    print(f"📈 Total emails: {len(CATEGORIES) * 5} (5 per category)")
    print("=" * 60)
    
    # User confirmation
    confirmation = input("\n⚠️  Do you really want to send all emails? (yes/no): ").lower().strip()
    if confirmation not in ['yes', 'y', 'ano', 'a']:
        print("❌ Sending cancelled by user")
        return
    
    sent_count = 0
    failed_count = 0
    start_time = datetime.now()
    
    # Track used subjects to avoid duplicates
    used_subjects = set()
    
    for category_name, category_data in CATEGORIES.items():
        print(f"\n📂 Sending emails for category: {category_name}")
        
        # Shuffle subjects and contents for variety
        subjects = category_data["subjects"].copy()
        contents = category_data["contents"].copy()
        random.shuffle(subjects)
        random.shuffle(contents)
        
        for i in range(5):  # 5 emails for each category
            # Generate random values for this email
            random_values = generate_random_values()
            
            # Pick subject and content
            subject_template = subjects[i % len(subjects)]
            content_template = contents[i % len(contents)]
            
            # Format subject with values
            try:
                subject = subject_template.format(**random_values)
            except KeyError:
                subject = subject_template
            
            # Ensure unique subject
            original_subject = subject
            counter = 1
            while subject in used_subjects:
                subject = f"{original_subject} ({counter})"
                counter += 1
            used_subjects.add(subject)
            
            # Format content with values
            try:
                content = content_template.format(**random_values)
            except KeyError:
                content = content_template
            
            # Add realistic signature
            content += create_realistic_signature(random_values)
            
            print(f"  📤 Email {i+1}/5: {subject[:60]}{'...' if len(subject) > 60 else ''}")
            
            # Send email
            if send_email(subject, content, RECIPIENT_EMAIL):
                sent_count += 1
                print(f"  ✅ Successfully sent")
            else:
                failed_count += 1
                print(f"  ❌ Error while sending")
                # If multiple emails fail, stop to avoid spam detection
                if failed_count >= 3:
                    print("⚠️  Too many failures, stopping to avoid spam detection")
                    break
            
            # Random pause between emails (1-4 seconds)
            time.sleep(random.uniform(1, 4))
        
        if failed_count >= 3:
            break
        
        # Longer pause between categories
        if category_name != list(CATEGORIES.keys())[-1]:  # Not last category
            pause = random.randint(3, 7)
            print(f"⏸️  Pausing {pause} seconds before next category...")
            time.sleep(pause)
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    print("\n" + "=" * 60)
    print("📊 SENDING SUMMARY:")
    print(f"✅ Successfully sent: {sent_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"📋 Total: {sent_count + failed_count}")
    print(f"⏱️  Duration: {duration}")
    print(f"📅 Completed: {end_time.strftime('%d.%m.%Y %H:%M:%S')}")
    print("=" * 60)
    
    if sent_count > 0:
        print(f"\n✨ Check your email inbox: {RECIPIENT_EMAIL}")
        print("💡 Tip: Some emails might be in spam folder")
        print("📁 You now have realistic test emails for your email sorting project!")

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