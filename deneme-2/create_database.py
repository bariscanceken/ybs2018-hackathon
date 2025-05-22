import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta

def create_database():
    try:
        # MySQL bağlantısı (veritabanı olmadan)
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='bariscan'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Veritabanını oluştur
            cursor.execute("DROP DATABASE IF EXISTS hackathon")
            cursor.execute("CREATE DATABASE hackathon")
            print("Veritabanı başarıyla oluşturuldu")
            
            # Veritabanını seç
            cursor.execute("USE hackathon")
            
            # Tabloları oluştur
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS kullanicilar (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    ad_soyad VARCHAR(255) NOT NULL,
                    eposta VARCHAR(255) NOT NULL UNIQUE,
                    rol VARCHAR(50) NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projeler (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    ad VARCHAR(255) NOT NULL,
                    aciklama TEXT,
                    baslangic_tarihi DATE,
                    bitis_tarihi DATE,
                    durum ENUM('Planlandı', 'Devam Ediyor', 'Tamamlandı') DEFAULT 'Planlandı',
                    oncelik ENUM('Düşük', 'Orta', 'Yüksek') DEFAULT 'Orta'
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS gorevler (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    baslik VARCHAR(255) NOT NULL,
                    aciklama TEXT,
                    baslangic_tarihi DATE,
                    bitis_tarihi DATE,
                    durum ENUM('Atandı', 'Devam Ediyor', 'Tamamlandı') DEFAULT 'Atandı',
                    oncelik ENUM('Düşük', 'Orta', 'Yüksek') DEFAULT 'Orta',
                    proje_id INT,
                    FOREIGN KEY (proje_id) REFERENCES projeler(id) ON DELETE CASCADE
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS raporlar (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    baslik VARCHAR(255) NOT NULL,
                    icerik TEXT,
                    rapor_tarihi DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS kullanici_gorev (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    kullanici_id INT,
                    gorev_id INT,
                    FOREIGN KEY (kullanici_id) REFERENCES kullanicilar(id) ON DELETE CASCADE,
                    FOREIGN KEY (gorev_id) REFERENCES gorevler(id) ON DELETE CASCADE
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS gorev_rapor (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    gorev_id INT,
                    rapor_id INT,
                    FOREIGN KEY (gorev_id) REFERENCES gorevler(id) ON DELETE CASCADE,
                    FOREIGN KEY (rapor_id) REFERENCES raporlar(id) ON DELETE CASCADE
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS proje_raporlar (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    proje_id INT,
                    rapor_id INT,
                    ilerleme_orani INT DEFAULT 0,
                    durum ENUM('Planlandı', 'Devam Ediyor', 'Tamamlandı') DEFAULT 'Devam Ediyor',
                    FOREIGN KEY (proje_id) REFERENCES projeler(id) ON DELETE CASCADE,
                    FOREIGN KEY (rapor_id) REFERENCES raporlar(id) ON DELETE CASCADE
                )
            """)

            print("Tablolar başarıyla oluşturuldu")
            
            # Örnek verileri ekle
            insert_sample_data(cursor)
            
    except Error as e:
        print(f"Hata: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL bağlantısı kapatıldı")

def insert_sample_data(cursor):
    # Örnek kullanıcılar
    users = [
        ("Ahmet Yılmaz", "ahmet@example.com", "Yönetici"),
        ("Ayşe Demir", "ayse@example.com", "Geliştirici"),
        ("Mehmet Kaya", "mehmet@example.com", "Test Uzmanı"),
        ("Zeynep Şahin", "zeynep@example.com", "Proje Yöneticisi")
    ]
    
    cursor.executemany("""
        INSERT INTO kullanicilar (ad_soyad, eposta, rol)
        VALUES (%s, %s, %s)
    """, users)
    
    # Örnek projeler
    projects = [
        ("E-Ticaret Platformu", "Online alışveriş platformu geliştirme", "Devam Ediyor", "Yüksek"),
        ("Mobil Uygulama", "iOS ve Android uygulaması geliştirme", "Planlandı", "Orta"),
        ("Web Sitesi Yenileme", "Kurumsal web sitesi yenileme projesi", "Devam Ediyor", "Düşük"),
        ("Veri Analizi Projesi", "Büyük veri analizi ve raporlama", "Tamamlandı", "Yüksek")
    ]
    
    cursor.executemany("""
        INSERT INTO projeler (ad, aciklama, durum, oncelik)
        VALUES (%s, %s, %s, %s)
    """, projects)
    
    # Örnek görevler
    tasks = [
        ("Veritabanı Tasarımı", "Veritabanı şeması oluşturma", "Devam Ediyor", "Yüksek", 1),
        ("Frontend Geliştirme", "Kullanıcı arayüzü geliştirme", "Atandı", "Orta", 1),
        ("API Geliştirme", "REST API endpoints oluşturma", "Devam Ediyor", "Yüksek", 2),
        ("Test Senaryoları", "Birim testleri yazma", "Atandı", "Orta", 2),
        ("Tasarım Çalışması", "UI/UX tasarımı", "Devam Ediyor", "Düşük", 3),
        ("İçerik Güncelleme", "Web sitesi içeriklerini güncelleme", "Atandı", "Orta", 3)
    ]
    
    cursor.executemany("""
        INSERT INTO gorevler (baslik, aciklama, durum, oncelik, proje_id)
        VALUES (%s, %s, %s, %s, %s)
    """, tasks)
    
    # Örnek raporlar
    reports = [
        ("Haftalık İlerleme Raporu", "Proje ilerleme durumu ve yapılan işler"),
        ("Test Sonuçları", "Birim testleri ve entegrasyon testleri sonuçları"),
        ("Performans Analizi", "Sistem performans metrikleri ve analizi"),
        ("Güvenlik Değerlendirmesi", "Güvenlik testleri ve risk analizi")
    ]
    
    cursor.executemany("""
        INSERT INTO raporlar (baslik, icerik)
        VALUES (%s, %s)
    """, reports)
    
    # Kullanıcı-Görev ilişkileri
    user_tasks = [
        (1, 1),  # Ahmet - Veritabanı Tasarımı
        (2, 2),  # Ayşe - Frontend Geliştirme
        (3, 3),  # Mehmet - API Geliştirme
        (4, 4),  # Zeynep - Test Senaryoları
        (1, 5),  # Ahmet - Tasarım Çalışması
        (2, 6)   # Ayşe - İçerik Güncelleme
    ]
    
    cursor.executemany("""
        INSERT INTO kullanici_gorev (kullanici_id, gorev_id)
        VALUES (%s, %s)
    """, user_tasks)
    
    # Proje-Rapor ilişkileri
    project_reports = [
        (1, 1, 75, "Devam Ediyor"),  # E-Ticaret - Haftalık Rapor
        (2, 2, 30, "Devam Ediyor"),  # Mobil Uygulama - Test Sonuçları
        (3, 3, 90, "Devam Ediyor"),  # Web Sitesi - Performans Analizi
        (4, 4, 100, "Tamamlandı")    # Veri Analizi - Güvenlik Değerlendirmesi
    ]
    
    cursor.executemany("""
        INSERT INTO proje_raporlar (proje_id, rapor_id, ilerleme_orani, durum)
        VALUES (%s, %s, %s, %s)
    """, project_reports)
    
    print("Örnek veriler başarıyla eklendi")

if __name__ == "__main__":
    create_database() 