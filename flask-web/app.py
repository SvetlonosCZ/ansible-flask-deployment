import json
import os
from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)
DATA_FILE = 'zpravy.json'

# --- Routa pro ÚVODNÍ STRÁNKU (index.html) ---
@app.route('/') 
def uvod():
    return render_template('index.html')

# --- Routa pro STRÁNKU KOČEK (kocky.html) ---
@app.route('/kocky')
def kocky():
    return render_template('kocky.html')

# --- Routa pro KONTAKTNÍ STRÁNKU A FORMULÁŘ (kontakt.html) ---
@app.route('/kontakt', methods=['GET', 'POST'])
def kontakt():
    
    success_message = request.args.get('success')
    error_message = None # Nová proměnná pro chybu
    
    # Předvyplníme proměnné pro případ, že vracíme formulář s chybou
    form_data = {
        'jmeno': '', 'prijmeni': '', 'datum': '', 'email': '', 
        'stat': '', 'pohlavi': '', 'zprava': ''
    }

    if request.method == 'POST':
        # 1. Získání dat z formuláře
        jmeno = request.form.get('jmeno')
        prijmeni = request.form.get('prijmeni')
        zprava = request.form.get('zprava')
        
        # Načteme i ostatní data, abychom je mohli vrátit
        form_data['jmeno'] = jmeno
        form_data['prijmeni'] = prijmeni
        form_data['zprava'] = zprava
        form_data['datum'] = request.form.get('datum')
        form_data['email'] = request.form.get('email')
        # ... atd. pro stat a pohlavi

        # 2. VALIDACE
        # Zkontrolujeme, zda povinná pole nejsou prázdná
        if not jmeno or not prijmeni or not zprava:
            # Pokud ano, nastavíme chybovou hlášku
            error_message = "Chyba: Jméno, příjmení a zpráva jsou povinná pole. Prosím, doplňte je."
            
            # Neuložíme data a rovnou znovu vykreslíme šablonu
            # DŮLEŽITÉ: Posíláme zpět data (form_data), aby se formulář předvyplnil
            return render_template('kontakt.html', 
                                   error_message=error_message, 
                                   **form_data) # ** rozbalí slovník na jmeno=jmeno, atd.

        # --- Pokud je validace v pořádku, pokračujeme v ukládání ---

        klic_zpravy = f"{prijmeni} {jmeno}"
        nova_zprava_data = {
            "email": form_data['email'],
            "datum_narozeni": form_data['datum'],
            "stat": request.form.get('stat'), # Načteme znovu
            "pohlavi": request.form.get('pohlavi'), # Načteme znovu
            "zprava": zprava,
        }

        # 3. Načtení existujících dat (pokud soubor existuje)
        data_slovnik = {}
        if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    data_slovnik = json.load(f)
            except json.JSONDecodeError:
                data_slovnik = {} # Soubor je poškozený nebo prázdný 
            except Exception as e:
                return f"Chyba při čtení JSON souboru: {e}"

        # 4. Přidání nových dat do slovníku
        if klic_zpravy not in data_slovnik: # Pokud klíč (Příjmení Jméno) ještě neexistuje, vytvoříme pro něj prázdný seznam
            data_slovnik[klic_zpravy] = []
        data_slovnik[klic_zpravy].append(nova_zprava_data)

        # 5. Uložení celého slovníku zpět do JSON souboru
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data_slovnik, f, ensure_ascii=False, indent=4)
            
            # 6. Přesměrování zpět na kontaktní stránku s hláškou o úspěchu
            return redirect(url_for('kontakt', success=True))
            
        except Exception as e:
            return f"Chyba při ukládání JSON na serveru: {e}"

    # Při prvním načtení stránky (GET)
    # Předáme proměnnou success_message a prázdná data do HTML šablony
    return render_template('kontakt.html', success_message=success_message, **form_data)

if __name__ == '__main__':
    app.run(debug=True)

