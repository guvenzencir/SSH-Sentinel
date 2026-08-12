# 🛡️ SSH-Sentinel: Active Brute-Force Defense & Threat Logging
*([Türkçe sürüm için aşağı kaydırın / Scroll down for Turkish version](#türkçe-sürüm))*

SSH-Sentinel is an autonomous Active Defense tool designed for Blue Team operations. It continuously monitors system authentication logs in real-time to detect SSH Brute-Force attacks. Upon detecting repeated failed login attempts from a single IP, it instantly blocks the attacker using `iptables` and logs the threat intelligence into a local MariaDB database.

## ✨ Features
*   **Real-Time Monitoring:** Silently tails the `/var/log/auth.log` file without consuming high system resources.
*   **Active Defense:** Instantly drops malicious connections by dynamically writing `iptables` rules.
*   **Autonomous Database Setup:** Automatically creates its own database (`sentinel_db`) and tables on the first run.
*   **CTI Logging:** Archives banned IP addresses and timestamps for future Cyber Threat Intelligence (CTI) analysis.

## 🚀 Installation & Usage

### 1. Requirements
*   Debian-based Linux (Ubuntu, Kali, etc.)
*   Python 3
*   MariaDB/MySQL server
*   `rsyslog` (for generating auth.log)

```bash
sudo apt update
sudo apt install rsyslog mariadb-server
pip install mysql-connector-python
```

### 2. Configuration
Open `ssh_sentinel.py` and update the database configuration with your root password:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_PASSWORD',
    'database': 'sentinel_db'
}
```

### 3. Execution
Since the script manipulates network firewalls via `iptables`, it must be run with root privileges:
```bash
sudo python3 ssh_sentinel.py
```

---
---

<a name="türkçe-sürüm"></a>
# 🛡️ SSH-Sentinel: Aktif Kaba Kuvvet Savunması ve Tehdit Loglama

SSH-Sentinel, Mavi Takım (Blue Team) operasyonları için geliştirilmiş otonom bir Aktif Savunma aracıdır. SSH Kaba Kuvvet (Brute-Force) saldırılarını tespit etmek için sistem kimlik doğrulama loglarını gerçek zamanlı olarak izler. Tek bir IP'den gelen tekrarlayan hatalı giriş denemelerini tespit ettiğinde, saldırganı `iptables` kullanarak anında engeller ve bu tehdit istihbaratını yerel bir MariaDB veritabanına kaydeder.

## ✨ Özellikler
*   **Gerçek Zamanlı İzleme:** Yüksek sistem kaynağı tüketmeden `/var/log/auth.log` dosyasını anlık olarak dinler.
*   **Aktif Savunma (Active Defense):** Dinamik `iptables` kuralları yazarak zararlı bağlantıları anında düşürür (DROP).
*   **Otonom Veritabanı Kurulumu:** İlk çalıştırıldığında kendi veritabanını (`sentinel_db`) ve tablolarını otomatik olarak oluşturur.
*   **CTI Loglama:** Gelecekteki Siber Tehdit İstihbaratı (CTI) analizleri için banlanan IP adreslerini ve zaman damgalarını arşivler.

## 🚀 Kurulum ve Kullanım

### 1. Gereksinimler
*   Debian tabanlı Linux (Ubuntu, Kali vb.)
*   Python 3
*   MariaDB/MySQL sunucusu
*   `rsyslog` (auth.log oluşturulması için)

```bash
sudo apt update
sudo apt install rsyslog mariadb-server
pip install mysql-connector-python
```

### 2. Konfigürasyon
`ssh_sentinel.py` dosyasını açın ve veritabanı ayarlarını kendi root şifrenizle güncelleyin:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_PASSWORD',
    'database': 'sentinel_db'
}
```

### 3. Çalıştırma
Betik, `iptables` üzerinden ağ güvenlik duvarına müdahale ettiği için root yetkileriyle çalıştırılmalıdır:
```bash
sudo python3 ssh_sentinel.py
```
