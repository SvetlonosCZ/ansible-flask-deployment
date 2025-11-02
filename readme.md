🤖 Ansible Flask Deployment - Praktický test a webová aplikace

📋 Popis projektu

Tento projekt automaticky konfiguruje server a nasazuje plně funkční dynamickou webovou aplikaci (Flask/Gunicorn), která zpracovává kontaktní formulář a ukládá data do souboru.

Konfigurace serveru a nasazení aplikace probíhá pomocí Ansible a zahrnuje:

✅ Instaluje a konfiguruje NGINX (jako reverzní proxy)

✅ Instaluje a konfiguruje Gunicorn a Systemd pro spuštění Flask aplikace

✅ Vytváří dedikovaného uživatele webappi pro bezpečný běh webové služby

✅ Nastavuje firewall UFW (povoleny pouze porty 22 a 80)

✅ Zabezpečuje SSH (zakázán root login, pouze SSH klíče)

✅ Instaluje Fail2ban a povoluje automatické bezpečnostní aktualizace

📁 Struktura projektu

Projekt má hybridní strukturu, kde je Flask aplikace v podsložce flask-web/ a Ansible struktura ji nasazuje.

ansible-project/
├── [vagrant]/
├── [group_vars]/
│   └── vault.yml
├── inventory/
│   └── hosts.yml
├── [playbooks]/
│   └── site.yml
├── [roles]/
│   ├── [system]/           # Role pro systémovou konfiguraci (UFW, SSH, Fail2ban)
│   └── [webserver]/        # Role pro NGINX, Gunicorn, Systemd a nasazení Flask
│       ├── [handlers]/
│       ├── [tasks]/
│       └── [templates]/
│           ├── nginx.conf.j2    # NGINX konfigurace (propojení na Gunicorn UNIX socket)
│           └── systemd.service.j2 # Systemd služba pro Gunicorn
│
├── flask-web/             # <--- SLOŽKA S FLASK APLIKACÍ
│   ├── app.py             # Flask routy a logika pro ukládání dat
│   └── ... (templates, static, requirements.txt)
│
├── Vagrantfile             # Vagrant konfigurace pro lokální testování
└── README.md               # Tento soubor



🚀 Jak spustit a nasadit

Prerekvizity

Vagrant 2.0+

VirtualBox 6.0+

Python (s nainstalovaným Ansible)

Lokální nasazení s Vagrant

Přejděte do kořenového adresáře

cd ansible-project



Spuštění VM a provisioning

vagrant up



(Tento krok provede kompletní konfiguraci serveru a nasazení Flask aplikace pod NGINX.)

Opakované spuštění Ansible (pokud už VM běží)

vagrant provision



Testování webové aplikace

# Z hostitelského počítače otestujte dostupnost aplikace
curl -I [http://192.168.56.10/kontakt](http://192.168.56.10/kontakt)



Očekávaný výstup: HTTP/1.1 200 OK

✅ Testování funkčnosti aplikace

Test 1: Ověření běhu Flask aplikace (Gunicorn/Systemd)

Ověřte, že služba pro Flask aplikaci běží a Gunicorn naslouchá na UNIX socketu.

vagrant ssh
sudo systemctl status flask_app.service



Test 2: Ověření datového toku (NGINX -> Gunicorn -> Flask)

Odešlete data do kontaktního formuláře, což spustí logiku pro ukládání dat.

vagrant ssh
curl -X POST http://localhost/kontakt \
     -d "jmeno=Testovac&prijmeni=Uzivatel" \
     -d "zprava=Toto je testovaci zprava" \
     -d "email=test@example.com"



Test 3: Ověření ukládání dat

Zkontrolujte, že se po odeslání dat vytvořil (nebo aktualizoval) soubor s uživatelskými zprávami.

vagrant ssh
cat /opt/static-sites/flask-web/zpravy.json



Ostatní testy (Firewall, SSH, Uživatel)

Test 4: Ověření firewallu

vagrant ssh
sudo ufw status



Test 5: Ověření SSH zabezpečení

vagrant ssh
sudo grep -E "PermitRootLogin|PasswordAuthentication" /etc/ssh/sshd_config



⚙️ Klíčové technické detaily

Protokol: Aplikace používá UNIX Socket (/run/gunicorn/gunicorn.sock) pro komunikaci mezi NGINX a Gunicornem.

Oprávnění: Díky nastavení RuntimeDirectoryGroup=www-data v Systemd službě má NGINX přístup k socketu pro zajištění bezproblémové komunikace.

Ukládání dat: Flask aplikace ukládá validní data z formuláře do souboru /opt/static-sites/flask-web/zpravy.json.

Webová adresa: Po nasazení je web dostupný na standardním HTTP portu 80.```

## 🔒 Bezpečnostní opatření

### Implementovaná opatření:
1. **UFW Firewall** - povoleny pouze porty 22 (SSH) a 80 (HTTP)
2. **SSH Hardening**:
   - Zakázáno přihlášení root uživatele
   - Zakázána autentizace heslem (pouze SSH klíče)
3. **Fail2ban** - ochrana proti brute-force útokům
4. **Unattended Upgrades** - automatické bezpečnostní aktualizace
5. **Dedikovaný uživatel** - webové soubory vlastní `webappi`, ne root

## 🔐 Ansible Vault

Citlivé hodnoty (hesla, SSH klíče) jsou uloženy v šifrovaném souboru `group_vars/vault.yml`.

### Struktura vault souboru:
```yaml
vault_webapp_password: "SuperTajneHeslo123!"
```

### Použití v produkci:

#### Spuštění playbooku s vault heslem:
```bash
ansible-playbook -i inventory/hosts.yml playbooks/site.yml --ask-vault-pass
```

#### Editace vault souboru:
```bash
ansible-vault edit group_vars/vault.yml
# Zadej vault heslo: admin123
```

#### Zobrazení obsahu:
```bash
ansible-vault view group_vars/vault.yml
```

#### Změna vault hesla:
```bash
ansible-vault rekey group_vars/vault.yml
```

### Pro Vagrant demo:
Vagrant používá **fallback hodnotu** (`DemoPassword123`) v `group_vars/all.yml`, takže není potřeba zadávat vault heslo při `vagrant provision`.

**Důležité:** Pro hashování hesel je potřeba knihovna `passlib`, která se automaticky instaluje při Vagrant provisioningu (viz `Vagrantfile` - shell provisioner).

V produkčním prostředí by se použilo:
- Environment proměnná `ANSIBLE_VAULT_PASSWORD`
- Soubor `--vault-password-file`
- Interaktivní prompt `--ask-vault-pass`

**Vault heslo pro testování:** `admin123`

### Proč Vault?
- ✅ Hesla nejsou v plain textu v Gitu
- ✅ Lze verzovat citlivé konfigurace bezpečně
- ✅ Podpora pro různá prostředí (dev, staging, prod)

---

## 🧩 Řešení technických problémů

### Passlib instalace
Ansible potřebuje knihovnu `passlib` pro hashování hesel. Ta se automaticky instaluje pomocí shell provisioneru ve Vagrantfile:
```ruby
config.vm.provision "shell", inline: <<-SHELL
  apt-get update -qq
  apt-get install -y python3-pip
  pip3 install passlib
SHELL
```

Tento krok zajišťuje, že při použití filtru `password_hash()` v Ansible tasků nebude chyba *"passlib must be installed"*.

## 📝 Poznámky

### Idempotence
Playbook je **idempotentní** - opakované spuštění neprovádí žádné změny, pokud je systém již ve správném stavu.

Ověření:
```bash
vagrant provision
# Očekávaný výstup: changed=0
```

### Ansible verze
Projekt vyžaduje Ansible 2.9+. Vagrant automaticky nainstaluje Ansible do VM pomocí `ansible_local` provisioneru.

## 🎯 Splněné požadavky

- ✅ Ansible best practices struktura
- ✅ Idempotentní playbook
- ✅ NGINX s vlastní konfigurací
- ✅ Webové soubory vlastněny uživatelem `webappi`
- ✅ Web dostupný na portu 80
- ✅ UFW firewall (porty 22, 80)
- ✅ SSH zabezpečení (no root, no password)
- ✅ Fail2ban a unattended-upgrades
- ✅ HTTP validace pomocí `uri` modulu

## 📧 Kontakt
**Autor**: [Marek Šlauf]  
**Email**: [mslauf@seznam.cz]  
**Datum**: 30.Říjen 2025