import sys
import os
import hashlib
from datetime import datetime
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QPushButton
import mysql.connector
from mysql.connector import Error

class GirisSayfasi(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # UI dosyasını yükle
        uic.loadUi('giris.ui', self)
        
        # Buton bağlantıları
        self.giris_button.clicked.connect(self.giris_yap)
        self.kayit_button.clicked.connect(self.kayit_sayfasina_git)
        
        # Veritabanı bağlantısı
        self.db_baglanti_kur()
        
    def db_baglanti_kur(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="bariscan",
                database="enesler"
            )
            self.cursor = self.conn.cursor()
        except Error as e:
            QMessageBox.critical(self, 'Veritabanı Hatası', f'MySQL bağlantı hatası: {str(e)}')
            sys.exit(1)
            
    def giris_yap(self):
        kullanici_adi = self.giris_kullaniciadi.text()
        sifre = self.giris_sifre.text()
        
        if not kullanici_adi or not sifre:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen kullanıcı adı ve şifre giriniz!')
            return
            
        try:
            # Şifreyi hashle
            hashed_sifre = hashlib.sha256(sifre.encode()).hexdigest()
            
            # Kullanıcıyı kontrol et
            self.cursor.execute("""
                SELECT id, ad, soyad FROM kullanicilar 
                WHERE kullanici_adi = %s AND sifre = %s
            """, (kullanici_adi, hashed_sifre))
            
            kullanici = self.cursor.fetchone()
            
            if kullanici:
                self.etkinlik_sayfasi = EtkinlikYonetimi(kullanici[0], kullanici[1], kullanici[2])
                self.etkinlik_sayfasi.show()
                self.close()
            else:
                QMessageBox.warning(self, 'Hata', 'Kullanıcı adı veya şifre hatalı!')
                
        except Error as e:
            QMessageBox.critical(self, 'Hata', f'Giriş yapılırken hata oluştu: {str(e)}')
            
    def kayit_sayfasina_git(self):
        self.kayit_sayfasi = KayitSayfasi()
        self.kayit_sayfasi.show()
        self.close()

class KayitSayfasi(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # UI dosyasını yükle
        uic.loadUi('kayit.ui', self)
        
        # Buton bağlantıları
        self.kayit_button.clicked.connect(self.kayit_ol)
        self.geri_button.clicked.connect(self.giris_sayfasina_don)
        
        # Veritabanı bağlantısı
        self.db_baglanti_kur()
        
    def db_baglanti_kur(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="bariscan",
                database="enesler"
            )
            self.cursor = self.conn.cursor()
        except Error as e:
            QMessageBox.critical(self, 'Veritabanı Hatası', f'MySQL bağlantı hatası: {str(e)}')
            sys.exit(1)
            
    def kayit_ol(self):
        ad = self.kayit_ad.text()
        soyad = self.kayit_soyad.text()
        email = self.kayit_email.text()
        kullanici_adi = self.kayit_kullaniciadi.text()
        sifre = self.kayit_sifre.text()
        sifre_tekrar = self.kayit_sifre_tekrar.text()
        
        # Boş alan kontrolü
        if not all([ad, soyad, email, kullanici_adi, sifre, sifre_tekrar]):
            QMessageBox.warning(self, 'Uyarı', 'Lütfen tüm alanları doldurunuz!')
            return
            
        # Şifre kontrolü
        if sifre != sifre_tekrar:
            QMessageBox.warning(self, 'Uyarı', 'Şifreler eşleşmiyor!')
            return
            
        try:
            # Şifreyi hashle
            hashed_sifre = hashlib.sha256(sifre.encode()).hexdigest()
            
            # Kullanıcıyı kaydet
            self.cursor.execute("""
                INSERT INTO kullanicilar (ad, soyad, email, kullanici_adi, sifre)
                VALUES (%s, %s, %s, %s, %s)
            """, (ad, soyad, email, kullanici_adi, hashed_sifre))
            
            self.conn.commit()
            QMessageBox.information(self, 'Başarılı', 'Kayıt başarıyla tamamlandı!')
            self.giris_sayfasina_don()
            
        except Error as e:
            if "Duplicate entry" in str(e):
                QMessageBox.warning(self, 'Hata', 'Bu kullanıcı adı veya e-posta zaten kullanılıyor!')
            else:
                QMessageBox.critical(self, 'Hata', f'Kayıt olurken hata oluştu: {str(e)}')
                
    def giris_sayfasina_don(self):
        self.giris_sayfasi = GirisSayfasi()
        self.giris_sayfasi.show()
        self.close()

class EtkinlikYonetimi(QtWidgets.QMainWindow):
    def __init__(self, kullanici_id, kullanici_ad, kullanici_soyad):
        super().__init__()
        # UI dosyasını yükle
        uic.loadUi('sayfa1.ui', self)
        
        # Kullanıcı bilgilerini sakla
        self.kullanici_id = kullanici_id
        self.kullanici_ad = kullanici_ad
        self.kullanici_soyad = kullanici_soyad
        
        # Pencere başlığını güncelle
        self.setWindowTitle(f"Etkinlik Yönetimi - {kullanici_ad} {kullanici_soyad}")
        
        # Veritabanı bağlantısı
        self.db_baglanti_kur()
        
        # Buton bağlantıları
        self.etkinlik_ekle.clicked.connect(self.etkinlik_ekle_fonksiyonu)
        self.etkinlik_duzenle.clicked.connect(self.etkinlik_duzenle_fonksiyonu)
        self.etkinlik_sil.clicked.connect(self.etkinlik_sil_fonksiyonu)
        
        # Tablo ayarları
        self.etkinlik_listesi.setColumnCount(5)  # Sütun sayısını 5'e çıkar
        self.etkinlik_listesi.setHorizontalHeaderLabels(['Etkinlik Adı', 'Yer', 'Tarih', 'Katılım', 'İşlemler'])
        self.etkinlik_listesi.setColumnWidth(0, 150)  # Etkinlik Adı
        self.etkinlik_listesi.setColumnWidth(1, 150)  # Yer
        self.etkinlik_listesi.setColumnWidth(2, 150)  # Tarih
        self.etkinlik_listesi.setColumnWidth(3, 100)  # Katılım
        self.etkinlik_listesi.setColumnWidth(4, 100)  # İşlemler
        
        # Etkinlikleri yükle
        self.etkinlikleri_yukle()
        
    def db_baglanti_kur(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="bariscan",
                database="enesler"
            )
            self.cursor = self.conn.cursor()
        except Error as e:
            QMessageBox.critical(self, 'Veritabanı Hatası', f'MySQL bağlantı hatası: {str(e)}')
            sys.exit(1)
            
    def etkinlikleri_yukle(self):
        try:
            # Tüm etkinlikleri getir
            self.cursor.execute("""
                SELECT e.*, 
                       CASE WHEN ek.id IS NOT NULL THEN 'Katılıyorum' ELSE 'Katılmıyorum' END as katilim_durumu,
                       ek.id as katilim_id
                FROM etkinlikler e
                LEFT JOIN etkinlik_katilimcilar ek ON e.id = ek.etkinlik_id AND ek.kullanici_id = %s
                ORDER BY e.tarih DESC
            """, (self.kullanici_id,))
            
            etkinlikler = self.cursor.fetchall()
            
            self.etkinlik_listesi.setRowCount(0)
            for etkinlik in etkinlikler:
                self.etkinlik_listesi.insertRow(self.etkinlik_listesi.rowCount())
                self.etkinlik_listesi.setItem(self.etkinlik_listesi.rowCount()-1, 0, 
                                            QTableWidgetItem(etkinlik[2]))  # ad
                self.etkinlik_listesi.setItem(self.etkinlik_listesi.rowCount()-1, 1, 
                                            QTableWidgetItem(etkinlik[3]))  # yer
                self.etkinlik_listesi.setItem(self.etkinlik_listesi.rowCount()-1, 2, 
                                            QTableWidgetItem(etkinlik[4].strftime('%d.%m.%Y %H:%M')))  # tarih
                
                # Katılım durumu
                katilim_item = QTableWidgetItem(etkinlik[7])  # katilim_durumu
                katilim_item.setTextAlignment(Qt.AlignCenter)
                self.etkinlik_listesi.setItem(self.etkinlik_listesi.rowCount()-1, 3, katilim_item)
                
                # Katılım butonu
                katilim_butonu = QPushButton('Katıl' if etkinlik[8] is None else 'Ayrıl')
                katilim_butonu.clicked.connect(lambda checked, e_id=etkinlik[0], k_id=etkinlik[8]: 
                                            self.etkinlige_katil(e_id, k_id))
                self.etkinlik_listesi.setCellWidget(self.etkinlik_listesi.rowCount()-1, 4, katilim_butonu)
                
        except Error as e:
            QMessageBox.critical(self, 'Hata', f'Etkinlikler yüklenirken hata oluştu: {str(e)}')
            
    def etkinlik_ekle_fonksiyonu(self):
        ad = self.etkinlik_adi.text()
        yer = self.etkinlik_yeri.text()
        tarih = self.etkinlik_tarihi.dateTime().toPyDateTime()
        aciklama = self.etkinlik_aciklama.toPlainText()
        
        if not ad or not yer:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen etkinlik adı ve yerini giriniz!')
            return
            
        try:
            self.cursor.execute("""
                INSERT INTO etkinlikler (kullanici_id, ad, yer, tarih, aciklama)
                VALUES (%s, %s, %s, %s, %s)
            """, (self.kullanici_id, ad, yer, tarih, aciklama))
            
            self.conn.commit()
            self.etkinlikleri_yukle()
            self.formu_temizle()
            QMessageBox.information(self, 'Başarılı', 'Etkinlik başarıyla eklendi!')
        except Error as e:
            QMessageBox.critical(self, 'Hata', f'Etkinlik eklenirken hata oluştu: {str(e)}')
        
    def etkinlik_duzenle_fonksiyonu(self):
        secili_satir = self.etkinlik_listesi.currentRow()
        if secili_satir < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen düzenlenecek etkinliği seçiniz!')
            return
            
        try:
            self.cursor.execute("""
                SELECT * FROM etkinlikler 
                WHERE kullanici_id = %s 
                ORDER BY tarih DESC 
                LIMIT 1 OFFSET %s
            """, (self.kullanici_id, secili_satir))
            
            etkinlik = self.cursor.fetchone()
            
            if etkinlik:
                # Form alanlarını doldur
                self.etkinlik_adi.setText(etkinlik[2])
                self.etkinlik_yeri.setText(etkinlik[3])
                self.etkinlik_tarihi.setDateTime(etkinlik[4])
                self.etkinlik_aciklama.setPlainText(etkinlik[5])
                
                # Eski etkinliği sil
                self.cursor.execute("DELETE FROM etkinlikler WHERE id = %s", (etkinlik[0],))
                self.conn.commit()
                
                self.etkinlikleri_yukle()
        except Error as e:
            QMessageBox.critical(self, 'Hata', f'Etkinlik düzenlenirken hata oluştu: {str(e)}')
        
    def etkinlik_sil_fonksiyonu(self):
        secili_satir = self.etkinlik_listesi.currentRow()
        if secili_satir < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen silinecek etkinliği seçiniz!')
            return
            
        try:
            # Seçili satırdaki etkinlik adını al
            etkinlik_adi = self.etkinlik_listesi.item(secili_satir, 0).text()
            
            # Etkinlik ID'sini bul
            self.cursor.execute("""
                SELECT id FROM etkinlikler 
                WHERE ad = %s AND kullanici_id = %s
            """, (etkinlik_adi, self.kullanici_id))
            
            etkinlik = self.cursor.fetchone()
            
            if not etkinlik:
                QMessageBox.warning(self, 'Hata', 'Etkinlik bulunamadı!')
                return
                
            etkinlik_id = etkinlik[0]
            
            cevap = QMessageBox.question(self, 'Onay', 
                                       f'"{etkinlik_adi}" etkinliğini silmek istediğinizden emin misiniz?',
                                       QMessageBox.Yes | QMessageBox.No)
            
            if cevap == QMessageBox.Yes:
                # Önce katılımcıları sil
                self.cursor.execute("DELETE FROM etkinlik_katilimcilar WHERE etkinlik_id = %s", (etkinlik_id,))
                # Sonra etkinliği sil
                self.cursor.execute("DELETE FROM etkinlikler WHERE id = %s", (etkinlik_id,))
                self.conn.commit()
                
                self.etkinlikleri_yukle()
                QMessageBox.information(self, 'Başarılı', 'Etkinlik başarıyla silindi!')
                
        except Error as e:
            QMessageBox.critical(self, 'Hata', f'Etkinlik silinirken hata oluştu: {str(e)}')
            
    def formu_temizle(self):
        self.etkinlik_adi.clear()
        self.etkinlik_yeri.clear()
        self.etkinlik_aciklama.clear()
        self.etkinlik_tarihi.setDateTime(datetime.now())
        
    def closeEvent(self, event):
        # Program kapatılırken veritabanı bağlantısını kapat
        if hasattr(self, 'conn') and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()

    def etkinlige_katil(self, etkinlik_id, katilim_id):
        try:
            if katilim_id is None:  # Katılım yoksa, katıl
                self.cursor.execute("""
                    INSERT INTO etkinlik_katilimcilar (etkinlik_id, kullanici_id)
                    VALUES (%s, %s)
                """, (etkinlik_id, self.kullanici_id))
                QMessageBox.information(self, 'Başarılı', 'Etkinliğe başarıyla katıldınız!')
            else:  # Katılım varsa, ayrıl
                self.cursor.execute("""
                    DELETE FROM etkinlik_katilimcilar 
                    WHERE etkinlik_id = %s AND kullanici_id = %s
                """, (etkinlik_id, self.kullanici_id))
                QMessageBox.information(self, 'Başarılı', 'Etkinlikten ayrıldınız!')
                
            self.conn.commit()
            self.etkinlikleri_yukle()
            
        except Error as e:
            QMessageBox.critical(self, 'Hata', f'İşlem sırasında hata oluştu: {str(e)}')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    giris = GirisSayfasi()
    giris.show()
    sys.exit(app.exec_()) 