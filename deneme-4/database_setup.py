# database_setup.py
import mysql.connector
from mysql.connector import Error
import bcrypt

# Veritabanı bağlantı bilgileri
DB_CONFIG = {
    "host": "localhost",
    "user": "root",  # MySQL kullanıcı adı
    "password": "bariscan",  # MySQL şifresi
    "database": "destek_db" # Kullanılacak veritabanı adı
}

def create_database():
    try:
        # MySQL bağlantısı
        connection = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )

        if connection.is_connected():
            cursor = connection.cursor()
            
            # Veritabanını oluştur
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
            cursor.execute(f"USE {DB_CONFIG['database']}")
            
            # Kullanıcılar tablosu
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS kullanicilar (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    ad_soyad VARCHAR(100) NOT NULL,
                    kullanici_adi VARCHAR(50) NOT NULL UNIQUE,
                    sifre VARCHAR(255) NOT NULL,
                    rol ENUM('talep', 'teknik') NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Destek talepleri tablosu
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS destek_talep (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    talep_sahibi_id INT NOT NULL,
                    kategori VARCHAR(50) NOT NULL,
                    baslik VARCHAR(200) NOT NULL,
                    aciklama TEXT NOT NULL,
                    oncelik ENUM('Düşük', 'Normal', 'Yüksek') NOT NULL,
                    durum ENUM('Beklemede', 'Devam Ediyor', 'Tamamlandı', 'İptal Edildi') NOT NULL,
                    olusturma_tarihi DATETIME NOT NULL,
                    cozum_tarihi DATETIME,
                    cozumu_yapan_id INT,
                    FOREIGN KEY (talep_sahibi_id) REFERENCES kullanicilar(id),
                    FOREIGN KEY (cozumu_yapan_id) REFERENCES kullanicilar(id)
                )
            """)
            
            print("Veritabanı ve tablolar başarıyla oluşturuldu!")
            
    except Error as e:
        print(f"Hata: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL bağlantısı kapatıldı.")

if __name__ == "__main__":
    print("Veritabanı kurulumu başlatılıyor...")
    create_database()
    print("Veritabanı kurulumu tamamlandı.")
