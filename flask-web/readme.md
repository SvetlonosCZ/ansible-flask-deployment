🌐 Osobní webová stránka (Python Flask)

🌟 Popis projektu

Jedná se o jednoduchou, plně responzivní webovou prezentaci vytvořenou s použitím moderního HTML5 a CSS3. Základní web je statický (index.html, kocky.html), ale obsahuje dynamický kontaktní formulář, jehož logika je zajištěna pomocí mikro-frameworku Flask v Pythonu.

Projekt demonstruje práci s:

✅ Flask Backend: routování stránek a zpracování dat formuláře na straně serveru.

✅ JSON Ukládání dat: data z formuláře se strukturovaně ukládají do souboru zpravy.json.

✅ Server-Side Validace: kontrola povinných polí (Jméno, Příjmení, Zpráva) a zobrazení chybové hlášky.

✅ Responzivní design (optimalizováno pro desktop i mobil).

📁 Struktura projektu

muj-flask-web/
├── app.py             # Hlavní serverová aplikace Flask
├── requirements.txt   # Závislosti (Flask)
├── README.md          # Tento soubor
├── templates/         # HTML šablony (index, kontakt, kocky)
└── static/            # CSS, obrázky a další statické zdroje


🚀 Jak spustit

Pro spuštění projektu potřebujete mít nainstalovaný Python 3.

Klonování repozitáře:

git clone <URL_VAŠEHO_REPOZITÁŘE>
cd muj-flask-web


Instalace závislostí:

Projekt vyžaduje pouze Flask. Je silně doporučeno použít virtuální prostředí.

# Vytvoření virtuálního prostředí
python3 -m venv venv 
# Aktivace prostředí (Mac/Linux)
source venv/bin/activate 
# Aktivace prostředí (Windows)
venv\Scripts\activate
# Instalace Flasku
pip install -r requirements.txt


Spuštění serveru:

python app.py


Otevření v prohlížeči:

Přejděte na adresu: http://127.0.0.1:5000/

Zastavení serveru:

V terminálu stiskněte Ctrl + C.

🛠️ Detaily Backendu

Aplikace app.py implementuje následující logiku:

Routy: / (uvod), /kontakt, /kocky.

Formulář: Na /kontakt zpracovává POST požadavek.

Validace: Kontroluje, zda jsou vyplněna pole jmeno, prijmeni a zprava. V případě chyby vrací formulář s červenou hláškou, přičemž zachovává již zadaná data.

Ukládání: Úspěšně odeslaná data se ukládají do souboru zpravy.json pod klíčem "Příjmení Jméno" pro snadnou agregaci.