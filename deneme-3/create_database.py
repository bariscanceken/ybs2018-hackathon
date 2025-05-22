import mysql.connector
from mysql.connector import Error
import hashlib

def create_database():
    try:
        # MySQL bağlantısı
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bariscan"
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Veritabanını oluştur
            cursor.execute("CREATE DATABASE IF NOT EXISTS enesler")
            cursor.execute("USE enesler")
            
            # Kullanıcılar tablosunu oluştur
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS kullanicilar (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    ad VARCHAR(50) NOT NULL,
                    soyad VARCHAR(50) NOT NULL,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    kullanici_adi VARCHAR(50) NOT NULL UNIQUE,
                    sifre VARCHAR(64) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Etkinlikler tablosunu oluştur
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS etkinlikler (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    kullanici_id INT NOT NULL,
                    ad VARCHAR(255) NOT NULL,
                    yer VARCHAR(255) NOT NULL,
                    tarih DATETIME NOT NULL,
                    aciklama TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (kullanici_id) REFERENCES kullanicilar(id)
                )
            """)
            
            # Etkinlik katılımcıları tablosunu oluştur
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS etkinlik_katilimcilar (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    etkinlik_id INT NOT NULL,
                    kullanici_id INT NOT NULL,
                    katilim_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (etkinlik_id) REFERENCES etkinlikler(id),
                    FOREIGN KEY (kullanici_id) REFERENCES kullanicilar(id)
                )
            """)
            
            # Örnek kullanıcılar
            kullanicilar = [
                ('Ahmet', 'Yılmaz', 'ahmet@email.com', 'ahmet', '123456'),
                ('Ayşe', 'Demir', 'ayse@email.com', 'ayse', '123456'),
                ('Mehmet', 'Kaya', 'mehmet@email.com', 'mehmet', '123456')
            ]
            
            # Kullanıcıları ekle
            for kullanici in kullanicilar:
                # Şifreyi hashle
                hashed_sifre = hashlib.sha256(kullanici[4].encode()).hexdigest()
                
                cursor.execute("""
                    INSERT INTO kullanicilar (ad, soyad, email, kullanici_adi, sifre)
                    VALUES (%s, %s, %s, %s, %s)
                """, (kullanici[0], kullanici[1], kullanici[2], kullanici[3], hashed_sifre))
            
            # Örnek etkinlikler
            etkinlikler = [
                (1, 'Yazılım Geliştirme Semineri', 'Online', '2024-04-15 14:00:00', 'Modern yazılım geliştirme teknikleri hakkında seminer'),
                (1, 'Python Workshop', 'İstanbul Teknik Üniversitesi', '2024-04-20 10:00:00', 'Python programlama dili workshop'),
                (2, 'Web Tasarım Kursu', 'Online', '2024-04-25 15:00:00', 'HTML, CSS ve JavaScript temelleri'),
                (3, 'Veri Bilimi Konferansı', 'Ankara Üniversitesi', '2024-05-01 09:00:00', 'Yapay zeka ve veri bilimi konferansı')
            ]
            
            # Etkinlikleri ekle
            for etkinlik in etkinlikler:
                cursor.execute("""
                    INSERT INTO etkinlikler (kullanici_id, ad, yer, tarih, aciklama)
                    VALUES (%s, %s, %s, %s, %s)
                """, etkinlik)
            
            # Örnek katılımcılar
            katilimcilar = [
                (1, 2),  # Ayşe, Yazılım Geliştirme Semineri'ne katılıyor
                (1, 3),  # Mehmet, Yazılım Geliştirme Semineri'ne katılıyor
                (2, 2),  # Ayşe, Python Workshop'a katılıyor
                (3, 1),  # Ahmet, Web Tasarım Kursu'na katılıyor
                (3, 3)   # Mehmet, Web Tasarım Kursu'na katılıyor
            ]
            
            # Katılımcıları ekle
            for katilimci in katilimcilar:
                cursor.execute("""
                    INSERT INTO etkinlik_katilimcilar (etkinlik_id, kullanici_id)
                    VALUES (%s, %s)
                """, katilimci)
            
            # Değişiklikleri kaydet
            connection.commit()
            print("Veritabanı ve tablolar başarıyla oluşturuldu!")
            print("Örnek veriler eklendi.")
            
    except Error as e:
        print(f"Veritabanı oluşturulurken hata oluştu: {str(e)}")
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL bağlantısı kapatıldı.")

if __name__ == "__main__":
    create_database() 