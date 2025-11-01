# Ansible NGINX Deployment - Praktický test

## 📋 Popis projektu
Tento projekt automaticky konfiguruje Ubuntu 22.04 server pomocí Ansible:
- ✅ Instaluje a konfiguruje NGINX webserver
- ✅ Vytváří dedikovaného uživatele `webappi` pro běh webové služby
- ✅ Nastavuje firewall UFW (povoleny pouze porty 22 a 80)
- ✅ Zabezpečuje SSH (zakázán root login, pouze SSH klíče)
- ✅ Instaluje Fail2ban (ochrana proti brute-force útokům)
- ✅ Povoluje automatické bezpečnostní aktualizace

## 📁 Struktura projektu
```
ansible-project/
├── [vagrant]/              # Vagrant runtime soubory
├── [group_vars]/
│   └── vault.yml           # Zahashované heslo
├── inventory/              
│   └── hosts.yml           # Definice cílových serverů
├── [playbooks]/
│   ├── [group_vars]/       # Proměnné pro všechny servery
│   │   └── all.yml         # Globální konfigurace
│   └── site.yml            # Hlavní playbook
├── [roles]/
│   ├── [system]/           # Role pro systémovou konfiguraci
│   │   ├── [handlers]/
│   │   │   └── main.yml    # SSH restart handler
│   │   └── [tasks]/
│   │       └── main.yml    # Systémové tasky
│   └── [webserver]/        # Role pro NGINX
│       ├── [handlers]/
│       │   └── main.yml    # NGINX restart handler
│       ├── [tasks]/
│       │   └── main.yml    # NGINX instalace a konfigurace
│       └── [templates]/
│           ├── nginx.conf.j2    # NGINX server config
│           └── index.html.j2    # Webová stránka
├── Vagrantfile             # Vagrant konfigurace pro lokální testování
└── README.md               # Tento soubor
```

## 🚀 Jak spustit

### Prerekvizity
- **Vagrant** 2.0+ ([stáhnout](https://www.vagrantup.com/downloads))
- **VirtualBox** 6.0+ ([stáhnout](https://www.virtualbox.org/wiki/Downloads))

### Lokální nasazení s Vagrant

1. **Klonování projektu**
```bash
git clone <URL_REPOZITARE>
cd ansible-project
```

2. **Spuštění VM a provisioning**
```bash
vagrant up
```

3. **Opakované spuštění Ansible (pokud už VM běží)**
```bash
vagrant provision
```

4. **SSH do VM**
```bash
vagrant ssh
```

5. **Zastavení VM**
```bash
vagrant halt
```

6. **Smazání VM**
```bash
vagrant destroy
```

## ✅ Testování funkčnosti

### Test 1: Ověření webového serveru
```bash
# Z hostitelského počítače
curl http://192.168.56.10

# Nebo v prohlížeči
http://192.168.56.10
```

Očekávaný výstup:
```html
<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <title>Practical Test - NGINX Deployment by webappi</title>
</head>
<body>
    <h1>Practical Test - NGINX Deployment by webappi</h1>
    <p>Tato stranka byla nasazena pomoci Ansible...</p>
</body>
</html>
```

### Test 2: Ověření firewallu
```bash
vagrant ssh
sudo ufw status
```

Očekávaný výstup:
```
Status: active

To                         Action      From
--                         ------      ----
22                         ALLOW       Anywhere
80                         ALLOW       Anywhere
```

### Test 3: Ověření NGINX služby
```bash
vagrant ssh
sudo systemctl status nginx
```

### Test 4: Ověření uživatele webappi
```bash
vagrant ssh
id webappi
ls -la /opt/static-sites
```

### Test 5: Ověření SSH zabezpečení
```bash
vagrant ssh
sudo grep -E "PermitRootLogin|PasswordAuthentication" /etc/ssh/sshd_config
```

Očekávaný výstup:
```
PermitRootLogin no
PasswordAuthentication no
```

## ⚙️ Konfigurace

Všechny proměnné jsou definovány v `playbooks/group_vars/all.yml`:
```yaml
webapp_user: webappi          # Uživatel pro běh webové služby
webapp_group: webappi         # Skupina uživatele
site_root_dir: /opt/static-sites  # Root adresář webu
site_title: "..."             # Titulek stránky
ssh_port: 22                  # SSH port
http_port: 80                 # HTTP port
```

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