import time
import subprocess
import re
import os
import mysql.connector
from mysql.connector import Error

LOG_FILE = "/var/log/auth.log"
MAX_ATTEMPTS = 5
BANNED_IPS = set()
ATTEMPTS_DICT = {}

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_PASSWORD', # ÖNEMLİ: Kendi MariaDB şifrenle değiştirmeyi unutma!
    'database': 'sentinel_db'
}

def setup_database():
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = connection.cursor()
        
        cursor.execute("CREATE DATABASE IF NOT EXISTS sentinel_db")
        cursor.execute("USE sentinel_db")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS banned_ips (
                id INT AUTO_INCREMENT PRIMARY KEY,
                ip_address VARCHAR(45) NOT NULL,
                ban_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.commit()
    except Error as e:
        print(f"[-] Database Error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def log_to_db(ip):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        insert_query = "INSERT INTO banned_ips (ip_address) VALUES (%s)"
        cursor.execute(insert_query, (ip,))
        connection.commit()
        
        print(f"[+] MariaDB Log: {ip} veritabanına işlendi. 📝\n")
    except Error as e:
        print(f"[-] DB Log Error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def block_ip(ip):
    if ip in BANNED_IPS:
        return
    
    print(f"\n[!] TEHLİKE: {ip} adresinden Brute-Force saldırısı tespit edildi!")
    print(f"[*] {ip} adresi iptables ile bloklanıyor...")
    
    subprocess.call(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])
    
    BANNED_IPS.add(ip)
    print(f"[+] Savunma başarılı. Saldırgan ({ip}) ağdan izole edildi.")
    
    log_to_db(ip)

def process_log_line(line):
    if "Failed password" in line or "Connection closed by authenticating user" in line:
        match = re.search(r'from (\d+\.\d+\.\d+\.\d+)', line)
        
        if match:
            attacker_ip = match.group(1)
            
            ATTEMPTS_DICT[attacker_ip] = ATTEMPTS_DICT.get(attacker_ip, 0) + 1
            deneme_sayisi = ATTEMPTS_DICT[attacker_ip]
            
            print(f"[*] Hatalı Giriş -> IP: {attacker_ip} | Deneme: {deneme_sayisi}/{MAX_ATTEMPTS}")
            
            if deneme_sayisi >= MAX_ATTEMPTS:
                block_ip(attacker_ip)

def monitor_logs():
    if os.geteuid() != 0:
        print("[-] HATA: Bu script iptables kullanacağı için 'sudo' yetkisiyle çalıştırılmalıdır.")
        return

    setup_database()
    print(f"[*] {LOG_FILE} dinleniyor... (Aktif Savunma & Veritabanı Loglama Devrede)")
    
    try:
        with open(LOG_FILE, "r") as f:
            f.seek(0, 2)
            
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.5)
                    continue
                
                process_log_line(line)
                
    except FileNotFoundError:
        print(f"[-] HATA: Log dosyası bulunamadı ({LOG_FILE}).")
    except KeyboardInterrupt:
        print("\n[*] Savunma kalkanı kapatıldı.")

if __name__ == "__main__":
    monitor_logs()
