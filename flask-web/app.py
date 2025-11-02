import os
import json
from datetime import datetime
from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)
# Důležité: Nyní se data ukládají jako JSON do kořenového adresáře aplikace.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'zpravy.json')

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
    error_message = None
    
    # KROK 1: VŽDY INITIALIZOVAT form_data s prázdnými defaultními hodnotami
    form_data = {
        'jmeno': '', 
        'prijmeni': '', 
        'datum': '', 
        'email': '', 
        'stat': 'Česká republika', 
        'pohlavi': 'muz',          
        'zprava': ''
    }
    
    # Načtení stávajících zpráv pro debug
    zpravy_data = {}
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                zpravy_data = json.load(f)
        except Exception:
            error_message = "Varování: Chyba při čtení zpravy.json. Pokračuji..."

    if request.method == 'POST':
        # 2. Získání dat z formuláře
        form_data.update(request.form.to_dict())

        # 3. VALIDACE
        if not form_data.get('jmeno') or not form_data.get('prijmeni') or not form_data.get('zprava'):
            error_message = "Chyba: Jméno, příjmení a zpráva jsou povinná pole. Prosím, doplňte je."
            
            # 1. VOLÁNÍ: POST se selháním validace
            return render_template('kontakt.html', 
                                   error_message=error_message, 
                                   zpravy_data=zpravy_data, 
                                   form_data=form_data) 


        # --- Ukládání dat ---

        klic_zpravy = f"{form_data['prijmeni']} {form_data['jmeno']}"
        
        nova_zprava_data = {
            'odeslano': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'email': form_data.get('email', 'N/A'),
            'datum_nar': form_data.get('datum', 'N/A'),
            'stat': form_data.get('stat', 'N/A'),
            'pohlavi': form_data.get('pohlavi', 'N/A'),
            'text': form_data['zprava']
        }
        
        data_slovnik = zpravy_data
        if klic_zpravy not in data_slovnik: 
            data_slovnik[klic_zpravy] = []
            
        data_slovnik[klic_zpravy].append(nova_zprava_data)

        # Uložení
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data_slovnik, f, ensure_ascii=False, indent=4)
            
            return redirect(url_for('kontakt', success=True))
            
        except Exception as e:
            error_message = f"Chyba při ukládání dat na serveru ({DATA_FILE}): {e}."
            
            # 2. VOLÁNÍ: POST se selháním ukládání
            return render_template('kontakt.html', 
                                   error_message=error_message, 
                                   zpravy_data=zpravy_data, 
                                   form_data=form_data) 


    # 3. VOLÁNÍ: GET POŽADAVEK
    return render_template('kontakt.html',
                           success_message=success_message,
                           error_message=error_message,
                           zpravy_data=zpravy_data,
                           form_data=form_data) 

if __name__ == '__main__':
    app.run(debug=True)
