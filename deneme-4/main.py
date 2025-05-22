# main.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QStackedWidget, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QTextEdit
)
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QFont
import mysql.connector
import bcrypt # Şifre güvenliği için eklendi
from datetime import datetime

# --- Veritabanı Yönetimi ---
class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return conn
        except mysql.connector.Error as err:
            QMessageBox.critical(None, "Veritabanı Bağlantı Hatası", f"Veritabanına bağlanılamadı: {err}\n"
                                                                   "Lütfen 'database_setup.py' dosyasını çalıştırdığınızdan ve MySQL sunucunuzun açık olduğundan emin olun.")
            return None

    def execute_query(self, query, params=None, fetch=False):
        conn = self.connect()
        if conn is None:
            return None if fetch else False

        cursor = conn.cursor()
        try:
            cursor.execute(query, params or ())
            if fetch:
                result = cursor.fetchall()
            else:
                conn.commit()
                result = True
            return result
        except mysql.connector.Error as err:
            QMessageBox.critical(None, "Veritabanı Hatası", f"Sorgu çalıştırılırken hata oluştu: {err}\nSorgu: {query}")
            return None if fetch else False
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

# --- Uygulama Stilleri ---
class AppStyles:
    PRIMARY_COLOR = "#4CAF50" # Yeşil
    ACCENT_COLOR = "#FFC107"  # Sarı
    BACKGROUND_COLOR = "#F5F5F5" # Açık gri
    TEXT_COLOR = "#333333"    # Koyu gri
    BORDER_RADIUS = "5px"
    BUTTON_HEIGHT = "40px"
    FONT_SIZE_TITLE = "28px"
    FONT_SIZE_SUBTITLE = "20px"
    FONT_SIZE_NORMAL = "16px"

    @staticmethod
    def get_main_window_style():
        return f"""
            QMainWindow {{
                background-color: {AppStyles.BACKGROUND_COLOR};
                font-family: 'Segoe UI', sans-serif;
            }}
            QPushButton {{
                background-color: {AppStyles.PRIMARY_COLOR};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: {AppStyles.BORDER_RADIUS};
                font-size: {AppStyles.FONT_SIZE_NORMAL};
                height: {AppStyles.BUTTON_HEIGHT};
            }}
            QPushButton:hover {{
                background-color: #45a049;
            }}
            QLineEdit, QTextEdit, QComboBox {{
                border: 1px solid #CCCCCC;
                border-radius: {AppStyles.BORDER_RADIUS};
                padding: 8px;
                font-size: {AppStyles.FONT_SIZE_NORMAL};
                background-color: white;
            }}
            QLabel {{
                color: {AppStyles.TEXT_COLOR};
                font-size: {AppStyles.FONT_SIZE_NORMAL};
            }}
            QTableWidget {{
                background-color: white;
                border: 1px solid #DDDDDD;
                border-radius: {AppStyles.BORDER_RADIUS};
                font-size: {AppStyles.FONT_SIZE_NORMAL};
                gridline-color: #EEEEEE;
            }}
            QHeaderView::section {{
                background-color: {AppStyles.PRIMARY_COLOR};
                color: white;
                padding: 5px;
                border: 1px solid {AppStyles.PRIMARY_COLOR};
                font-size: {AppStyles.FONT_SIZE_NORMAL};
            }}
        """

# --- UI Sınıfları ---

class Ui_GirisSayfasi(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(20)

        title = QLabel("Destek Sistemi Giriş")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {AppStyles.PRIMARY_COLOR};")
        self.layout.addWidget(title)

        self.kullanici_adi_input = QLineEdit()
        self.kullanici_adi_input.setPlaceholderText("Kullanıcı Adı")
        self.layout.addWidget(self.kullanici_adi_input)

        self.sifre_input = QLineEdit()
        self.sifre_input.setPlaceholderText("Şifre")
        self.sifre_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.sifre_input)

        self.giris_button = QPushButton("Giriş Yap")
        self.layout.addWidget(self.giris_button)

        self.personel_kayit_button = QPushButton("Personel Kayıt Ol")
        self.personel_kayit_button.setStyleSheet(f"background-color: {AppStyles.ACCENT_COLOR};")
        self.layout.addWidget(self.personel_kayit_button)

        self.musteri_kayit_button = QPushButton("Müşteri Kayıt Ol")
        self.musteri_kayit_button.setStyleSheet(f"background-color: {AppStyles.ACCENT_COLOR};")
        self.layout.addWidget(self.musteri_kayit_button)

class Ui_MusteriKayit(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(15)

        title = QLabel("Müşteri Kayıt")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {AppStyles.PRIMARY_COLOR};")
        self.layout.addWidget(title)

        self.ad_soyad_input = QLineEdit()
        self.ad_soyad_input.setPlaceholderText("Ad Soyad")
        self.layout.addWidget(self.ad_soyad_input)

        self.kullanici_adi_input = QLineEdit()
        self.kullanici_adi_input.setPlaceholderText("Kullanıcı Adı (Benzersiz)")
        self.layout.addWidget(self.kullanici_adi_input)

        self.sifre_input = QLineEdit()
        self.sifre_input.setPlaceholderText("Şifre")
        self.sifre_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.sifre_input)

        self.kayit_button = QPushButton("Müşteri Olarak Kaydol")
        self.layout.addWidget(self.kayit_button)

        self.geri_button = QPushButton("Geri Dön")
        self.geri_button.setStyleSheet(f"background-color: #6c757d;")
        self.layout.addWidget(self.geri_button)

class Ui_PersonelKayit(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(15)

        title = QLabel("Personel Kayıt")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {AppStyles.PRIMARY_COLOR};")
        self.layout.addWidget(title)

        self.ad_soyad_input = QLineEdit()
        self.ad_soyad_input.setPlaceholderText("Ad Soyad")
        self.layout.addWidget(self.ad_soyad_input)

        self.kullanici_adi_input = QLineEdit()
        self.kullanici_adi_input.setPlaceholderText("Kullanıcı Adı (Benzersiz)")
        self.layout.addWidget(self.kullanici_adi_input)

        self.sifre_input = QLineEdit()
        self.sifre_input.setPlaceholderText("Şifre")
        self.sifre_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.sifre_input)

        self.kayit_button = QPushButton("Personel Olarak Kaydol")
        self.layout.addWidget(self.kayit_button)

        self.geri_button = QPushButton("Geri Dön")
        self.geri_button.setStyleSheet(f"background-color: #6c757d;")
        self.layout.addWidget(self.geri_button)

class Ui_MusteriSayfasi(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        top_row_layout = QHBoxLayout()
        self.welcome_label = QLabel("Hoş Geldiniz, [Kullanıcı Adı]")
        self.welcome_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.welcome_label.setStyleSheet(f"color: {AppStyles.TEXT_COLOR};")
        top_row_layout.addWidget(self.welcome_label)
        top_row_layout.addStretch()

        self.logout_button = QPushButton("Çıkış Yap")
        self.logout_button.setStyleSheet(f"background-color: #dc3545;") # Kırmızı
        top_row_layout.addWidget(self.logout_button)
        self.layout.addLayout(top_row_layout)

        self.yeni_talep_button = QPushButton("Yeni Talep Oluştur")
        self.layout.addWidget(self.yeni_talep_button)

        self.talep_list_label = QLabel("Taleplerim")
        self.talep_list_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.layout.addWidget(self.talep_list_label)

        self.request_table = QTableWidget()
        self.request_table.setColumnCount(6) # ID, Başlık, Kategori, Açıklama, Öncelik, Durum, Oluşturma Tarihi
        self.request_table.setHorizontalHeaderLabels(["ID", "Başlık", "Kategori", "Öncelik", "Durum", "Tarih"])
        self.request_table.horizontalHeader().setStretchLastSection(True)
        self.request_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.request_table.setEditTriggers(QTableWidget.NoEditTriggers) # Düzenlemeyi devre dışı bırak
        self.layout.addWidget(self.request_table)

class Ui_YeniTalepSayfasi(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        title = QLabel("Yeni Destek Talebi Oluştur")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {AppStyles.PRIMARY_COLOR};")
        self.layout.addWidget(title)

        # Kategori
        self.kategori_label = QLabel("Kategori:")
        self.layout.addWidget(self.kategori_label)
        self.kategori_combo = QComboBox()
        self.kategori_combo.addItems(["Yazılım", "Donanım", "Ağ", "Diğer"])
        self.layout.addWidget(self.kategori_combo)

        # Başlık
        self.baslik_label = QLabel("Başlık:")
        self.layout.addWidget(self.baslik_label)
        self.baslik_input = QLineEdit()
        self.baslik_input.setPlaceholderText("Talebinizin kısa başlığı")
        self.layout.addWidget(self.baslik_input)

        # Açıklama
        self.aciklama_label = QLabel("Açıklama:")
        self.layout.addWidget(self.aciklama_label)
        self.aciklama_text = QTextEdit()
        self.aciklama_text.setPlaceholderText("Talebinizin detaylı açıklaması...")
        self.layout.addWidget(self.aciklama_text)

        # Öncelik
        self.oncelik_label = QLabel("Öncelik:")
        self.layout.addWidget(self.oncelik_label)
        self.oncelik_combo = QComboBox()
        self.oncelik_combo.addItems(["Düşük", "Normal", "Yüksek"])
        self.layout.addWidget(self.oncelik_combo)

        self.talep_olustur_button = QPushButton("Talebi Oluştur")
        self.layout.addWidget(self.talep_olustur_button)

        self.geri_button = QPushButton("Geri Dön")
        self.geri_button.setStyleSheet(f"background-color: #6c757d;")
        self.layout.addWidget(self.geri_button)

class Ui_PersonelSayfasi(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        top_row_layout = QHBoxLayout()
        self.welcome_label = QLabel("Hoş Geldiniz, [Personel Adı]")
        self.welcome_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.welcome_label.setStyleSheet(f"color: {AppStyles.TEXT_COLOR};")
        top_row_layout.addWidget(self.welcome_label)
        top_row_layout.addStretch()

        self.logout_button = QPushButton("Çıkış Yap")
        self.logout_button.setStyleSheet(f"background-color: #dc3545;") # Kırmızı
        top_row_layout.addWidget(self.logout_button)
        self.layout.addLayout(top_row_layout)

        self.talep_list_label = QLabel("Tüm Talepler")
        self.talep_list_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.layout.addWidget(self.talep_list_label)

        # Arama ve Filtreleme
        filter_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Talep ID, Başlık veya Açıklama Ara...")
        filter_layout.addWidget(self.search_input)
        self.search_button = QPushButton("Ara")
        filter_layout.addWidget(self.search_button)
        self.layout.addLayout(filter_layout)

        self.request_table = QTableWidget()
        self.request_table.setColumnCount(9) # ID, Talep Sahibi, Kategori, Başlık, Açıklama, Öncelik, Durum, Oluşturma Tarihi, Çözüm Tarihi, Çözen Personel
        self.request_table.setHorizontalHeaderLabels([
            "ID", "Talep Sahibi", "Kategori", "Başlık", "Açıklama", "Öncelik", "Durum", "Oluşturma Tarihi", "Çözüm Tarihi", "Çözen Personel"
        ])
        self.request_table.horizontalHeader().setStretchLastSection(True)
        self.request_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.request_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout.addWidget(self.request_table)

        # Talep Yönetim Butonları
        button_layout = QHBoxLayout()
        self.talep_sec_label = QLabel("Seçili Talep ID: Yok")
        self.talep_sec_label.setFont(QFont("Segoe UI", 12))
        button_layout.addWidget(self.talep_sec_label)
        button_layout.addStretch() # Sol tarafı itmek için

        self.update_status_combo = QComboBox()
        self.update_status_combo.addItems(["Beklemede", "Devam Ediyor", "Tamamlandı", "İptal Edildi"])
        self.update_status_combo.setCurrentText("Beklemede")
        button_layout.addWidget(self.update_status_combo)

        self.update_talep_button = QPushButton("Durumu Güncelle")
        button_layout.addWidget(self.update_talep_button)

        self.delete_talep_button = QPushButton("Talebi Sil")
        self.delete_talep_button.setStyleSheet(f"background-color: #dc3545;")
        button_layout.addWidget(self.delete_talep_button)
        self.layout.addLayout(button_layout)


# --- Ana Pencere ve Sayfa Geçişleri ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Destek Sistemi")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet(AppStyles.get_main_window_style())

        # Veritabanı bağlantısı
        self.db = DatabaseManager(
            host="localhost",
            user="root",
            password="bariscan",
            database="destek_db"
        )

        self.current_user_id = None
        self.current_user_role = None
        self.current_user_name = None
        self.selected_request_id = None # Personel sayfasında seçilen talep ID'si

        self.stackedWidget = QStackedWidget()
        self.setCentralWidget(self.stackedWidget)

        self.ui_giris = Ui_GirisSayfasi()
        self.ui_musteri_kayit = Ui_MusteriKayit()
        self.ui_personel_kayit = Ui_PersonelKayit()
        self.ui_musteri_sayfasi = Ui_MusteriSayfasi()
        self.ui_personel_sayfasi = Ui_PersonelSayfasi()
        self.ui_yeni_talep_sayfasi = Ui_YeniTalepSayfasi()

        self.stackedWidget.addWidget(self.ui_giris)
        self.stackedWidget.addWidget(self.ui_musteri_kayit)
        self.stackedWidget.addWidget(self.ui_personel_kayit)
        self.stackedWidget.addWidget(self.ui_musteri_sayfasi)
        self.stackedWidget.addWidget(self.ui_personel_sayfasi)
        self.stackedWidget.addWidget(self.ui_yeni_talep_sayfasi)

        self.init_connections()
        self.show_giris_sayfasi()

    def init_connections(self):
        # Giriş Sayfası Bağlantıları
        self.ui_giris.giris_button.clicked.connect(self.handle_giris)
        self.ui_giris.personel_kayit_button.clicked.connect(self.show_personel_kayit_sayfasi)
        self.ui_giris.musteri_kayit_button.clicked.connect(self.show_musteri_kayit_sayfasi)

        # Müşteri Kayıt Sayfası Bağlantıları
        self.ui_musteri_kayit.kayit_button.clicked.connect(self.handle_musteri_kayit)
        self.ui_musteri_kayit.geri_button.clicked.connect(self.show_giris_sayfasi)

        # Personel Kayıt Sayfası Bağlantıları
        self.ui_personel_kayit.kayit_button.clicked.connect(self.handle_personel_kayit)
        self.ui_personel_kayit.geri_button.clicked.connect(self.show_giris_sayfasi)

        # Müşteri Sayfası Bağlantıları
        self.ui_musteri_sayfasi.logout_button.clicked.connect(self.handle_logout)
        self.ui_musteri_sayfasi.yeni_talep_button.clicked.connect(self.show_yeni_talep_sayfasi)

        # Yeni Talep Sayfası Bağlantıları
        self.ui_yeni_talep_sayfasi.talep_olustur_button.clicked.connect(self.handle_yeni_talep_kaydet)
        self.ui_yeni_talep_sayfasi.geri_button.clicked.connect(self.show_musteri_sayfasi)

        # Personel Sayfası Bağlantıları
        self.ui_personel_sayfasi.logout_button.clicked.connect(self.handle_logout)
        self.ui_personel_sayfasi.search_button.clicked.connect(self.load_all_requests_personnel)
        self.ui_personel_sayfasi.request_table.cellClicked.connect(self.handle_personnel_table_selection)
        self.ui_personel_sayfasi.update_talep_button.clicked.connect(self.handle_update_talep_durum)
        self.ui_personel_sayfasi.delete_talep_button.clicked.connect(self.handle_delete_talep)


    # --- Sayfa Gösterim Fonksiyonları ---
    def show_giris_sayfasi(self):
        self.ui_giris.kullanici_adi_input.clear()
        self.ui_giris.sifre_input.clear()
        self.stackedWidget.setCurrentWidget(self.ui_giris)

    def show_musteri_kayit_sayfasi(self):
        self.ui_musteri_kayit.ad_soyad_input.clear()
        self.ui_musteri_kayit.kullanici_adi_input.clear()
        self.ui_musteri_kayit.sifre_input.clear()
        self.stackedWidget.setCurrentWidget(self.ui_musteri_kayit)

    def show_personel_kayit_sayfasi(self):
        self.ui_personel_kayit.ad_soyad_input.clear()
        self.ui_personel_kayit.kullanici_adi_input.clear()
        self.ui_personel_kayit.sifre_input.clear()
        self.stackedWidget.setCurrentWidget(self.ui_personel_kayit)

    def show_musteri_sayfasi(self):
        if self.current_user_name:
            self.ui_musteri_sayfasi.welcome_label.setText(f"Hoş Geldiniz, {self.current_user_name}")
        self.load_customer_requests()
        self.stackedWidget.setCurrentWidget(self.ui_musteri_sayfasi)

    def show_personel_sayfasi(self):
        if self.current_user_name:
            self.ui_personel_sayfasi.welcome_label.setText(f"Hoş Geldiniz, {self.current_user_name}")
        self.load_all_requests_personnel()
        self.stackedWidget.setCurrentWidget(self.ui_personel_sayfasi)

    def show_yeni_talep_sayfasi(self):
        self.ui_yeni_talep_sayfasi.baslik_input.clear()
        self.ui_yeni_talep_sayfasi.aciklama_text.clear()
        self.ui_yeni_talep_sayfasi.kategori_combo.setCurrentIndex(0)
        self.ui_yeni_talep_sayfasi.oncelik_combo.setCurrentIndex(0)
        self.stackedWidget.setCurrentWidget(self.ui_yeni_talep_sayfasi)

    # --- İşlem Fonksiyonları ---

    def handle_giris(self):
        kullanici_adi = self.ui_giris.kullanici_adi_input.text().strip()
        sifre = self.ui_giris.sifre_input.text().strip()

        if not kullanici_adi or not sifre:
            QMessageBox.warning(self, "Giriş Hatası", "Kullanıcı adı ve şifre boş bırakılamaz.")
            return

        query = "SELECT id, ad_soyad, sifre, rol FROM kullanicilar WHERE kullanici_adi = %s"
        user_data = self.db.execute_query(query, (kullanici_adi,), fetch=True)

        if user_data:
            user_id, ad_soyad, hashed_sifre, rol = user_data[0]
            # Bcrypt ile şifre kontrolü
            if bcrypt.checkpw(sifre.encode('utf-8'), hashed_sifre.encode('utf-8')):
                self.current_user_id = user_id
                self.current_user_role = rol
                self.current_user_name = ad_soyad
                QMessageBox.information(self, "Giriş Başarılı", f"Hoş geldiniz, {ad_soyad}!")
                if rol == "talep":
                    self.show_musteri_sayfasi()
                elif rol == "teknik":
                    self.show_personel_sayfasi()
            else:
                QMessageBox.warning(self, "Giriş Hatası", "Kullanıcı adı veya şifre hatalı.")
        else:
            QMessageBox.warning(self, "Giriş Hatası", "Kullanıcı adı veya şifre hatalı.")

    def handle_musteri_kayit(self):
        ad_soyad = self.ui_musteri_kayit.ad_soyad_input.text().strip()
        kullanici_adi = self.ui_musteri_kayit.kullanici_adi_input.text().strip()
        sifre = self.ui_musteri_kayit.sifre_input.text().strip()
        rol = "talep" # Müşteri olduğu için rol sabit

        if not ad_soyad or not kullanici_adi or not sifre:
            QMessageBox.warning(self, "Kayıt Hatası", "Tüm alanlar doldurulmalıdır.")
            return

        # Kullanıcı adı zaten var mı kontrol et
        check_query = "SELECT COUNT(*) FROM kullanicilar WHERE kullanici_adi = %s"
        if self.db.execute_query(check_query, (kullanici_adi,), fetch=True)[0][0] > 0:
            QMessageBox.warning(self, "Kayıt Hatası", "Bu kullanıcı adı zaten alınmış. Lütfen başka bir kullanıcı adı deneyin.")
            return

        # Şifreyi hashle
        hashed_sifre = bcrypt.hashpw(sifre.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        insert_query = """
        INSERT INTO kullanicilar (ad_soyad, kullanici_adi, sifre, rol)
        VALUES (%s, %s, %s, %s)
        """
        if self.db.execute_query(insert_query, (ad_soyad, kullanici_adi, hashed_sifre, rol)):
            QMessageBox.information(self, "Kayıt Başarılı", "Müşteri kaydınız başarıyla oluşturuldu!")
            self.show_giris_sayfasi()
        else:
            QMessageBox.critical(self, "Kayıt Hatası", "Müşteri kaydı sırasında bir hata oluştu.")

    def handle_personel_kayit(self):
        ad_soyad = self.ui_personel_kayit.ad_soyad_input.text().strip()
        kullanici_adi = self.ui_personel_kayit.kullanici_adi_input.text().strip()
        sifre = self.ui_personel_kayit.sifre_input.text().strip()
        rol = "teknik" # Personel olduğu için rol sabit

        if not ad_soyad or not kullanici_adi or not sifre:
            QMessageBox.warning(self, "Kayıt Hatası", "Tüm alanlar doldurulmalıdır.")
            return

        # Kullanıcı adı zaten var mı kontrol et
        check_query = "SELECT COUNT(*) FROM kullanicilar WHERE kullanici_adi = %s"
        if self.db.execute_query(check_query, (kullanici_adi,), fetch=True)[0][0] > 0:
            QMessageBox.warning(self, "Kayıt Hatası", "Bu kullanıcı adı zaten alınmış. Lütfen başka bir kullanıcı adı deneyin.")
            return

        # Şifreyi hashle
        hashed_sifre = bcrypt.hashpw(sifre.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        insert_query = """
        INSERT INTO kullanicilar (ad_soyad, kullanici_adi, sifre, rol)
        VALUES (%s, %s, %s, %s)
        """
        if self.db.execute_query(insert_query, (ad_soyad, kullanici_adi, hashed_sifre, rol)):
            QMessageBox.information(self, "Kayıt Başarılı", "Personel kaydınız başarıyla oluşturuldu!")
            self.show_giris_sayfasi()
        else:
            QMessageBox.critical(self, "Kayıt Hatası", "Personel kaydı sırasında bir hata oluştu.")

    def handle_logout(self):
        self.current_user_id = None
        self.current_user_role = None
        self.current_user_name = None
        QMessageBox.information(self, "Çıkış Yapıldı", "Başarıyla çıkış yaptınız.")
        self.show_giris_sayfasi()

    def handle_yeni_talep_kaydet(self):
        if self.current_user_id is None:
            QMessageBox.warning(self, "Hata", "Talep oluşturmak için giriş yapmalısınız.")
            self.show_giris_sayfasi()
            return

        kategori = self.ui_yeni_talep_sayfasi.kategori_combo.currentText()
        baslik = self.ui_yeni_talep_sayfasi.baslik_input.text().strip()
        aciklama = self.ui_yeni_talep_sayfasi.aciklama_text.toPlainText().strip()
        oncelik = self.ui_yeni_talep_sayfasi.oncelik_combo.currentText()
        durum = "Beklemede" # Yeni talep varsayılan olarak "Beklemede"

        if not baslik or not aciklama:
            QMessageBox.warning(self, "Hata", "Başlık ve Açıklama alanları boş bırakılamaz.")
            return

        olusturma_tarihi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        query = """
        INSERT INTO destek_talep (talep_sahibi_id, kategori, baslik, aciklama, oncelik, durum, olusturma_tarihi)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (self.current_user_id, kategori, baslik, aciklama, oncelik, durum, olusturma_tarihi)

        if self.db.execute_query(query, params):
            QMessageBox.information(self, "Başarılı", "Talep başarıyla kaydedildi.")
            self.show_musteri_sayfasi() # Talebi kaydettikten sonra müşteri sayfasına geri dön
        else:
            QMessageBox.critical(self, "Hata", "Talep kaydedilirken bir sorun oluştu.")

    def load_customer_requests(self):
        if self.current_user_id is None:
            self.ui_musteri_sayfasi.request_table.setRowCount(0)
            return

        query = """
        SELECT id, baslik, kategori, aciklama, oncelik, durum, olusturma_tarihi
        FROM destek_talep
        WHERE talep_sahibi_id = %s
        ORDER BY olusturma_tarihi DESC
        """
        requests = self.db.execute_query(query, (self.current_user_id,), fetch=True)

        self.ui_musteri_sayfasi.request_table.setRowCount(0) # Tabloyu temizle
        if requests:
            self.ui_musteri_sayfasi.request_table.setRowCount(len(requests))
            for row_idx, req in enumerate(requests):
                self.ui_musteri_sayfasi.request_table.setItem(row_idx, 0, QTableWidgetItem(str(req[0]))) # ID
                self.ui_musteri_sayfasi.request_table.setItem(row_idx, 1, QTableWidgetItem(req[1])) # Başlık
                self.ui_musteri_sayfasi.request_table.setItem(row_idx, 2, QTableWidgetItem(req[2])) # Kategori
                # Müşteri sayfasında açıklamayı göstermeye gerek yok, detay için tıklayabilir
                self.ui_musteri_sayfasi.request_table.setItem(row_idx, 3, QTableWidgetItem(req[4])) # Öncelik (req[3] açıklamaydı, şimdi başlık ve aciklama arasında yer değişti)
                self.ui_musteri_sayfasi.request_table.setItem(row_idx, 4, QTableWidgetItem(req[5])) # Durum
                self.ui_musteri_sayfasi.request_table.setItem(row_idx, 5, QTableWidgetItem(str(req[6]))) # Oluşturma Tarihi
        else:
            QMessageBox.information(self, "Bilgi", "Henüz bir talebiniz bulunmamaktadır.")

    def load_all_requests_personnel(self):
        search_text = self.ui_personel_sayfasi.search_input.text().strip()
        query = """
        SELECT
            dt.id,
            k_sahip.ad_soyad AS talep_sahibi_ad_soyad,
            dt.kategori,
            dt.baslik,
            dt.aciklama,
            dt.oncelik,
            dt.durum,
            dt.olusturma_tarihi,
            dt.cozum_tarihi,
            k_cozen.ad_soyad AS cozumu_yapan_ad_soyad
        FROM
            destek_talep dt
        JOIN
            kullanicilar k_sahip ON dt.talep_sahibi_id = k_sahip.id
        LEFT JOIN
            kullanicilar k_cozen ON dt.cozumu_yapan_id = k_cozen.id
        WHERE
            dt.id LIKE %s OR dt.baslik LIKE %s OR dt.aciklama LIKE %s
        ORDER BY dt.olusturma_tarihi DESC
        """
        search_param = f"%{search_text}%"
        requests = self.db.execute_query(query, (search_param, search_param, search_param), fetch=True)

        self.ui_personel_sayfasi.request_table.setRowCount(0) # Tabloyu temizle
        if requests:
            self.ui_personel_sayfasi.request_table.setRowCount(len(requests))
            for row_idx, req in enumerate(requests):
                self.ui_personel_sayfasi.request_table.setItem(row_idx, 0, QTableWidgetItem(str(req[0]))) # ID
                self.ui_personel_sayfasi.request_table.setItem(row_idx, 1, QTableWidgetItem(req[1])) # Talep Sahibi Ad Soyad
                self.ui_personel_sayfasi.request_table.setItem(row_idx, 2, QTableWidgetItem(req[2])) # Kategori
                self.ui_personel_sayfasi.request_table.setItem(row_idx, 3, QTableWidgetItem(req[3])) # Başlık
                self.ui_personel_sayfasi.request_table.setItem(row_idx, 4, QTableWidgetItem(req[4])) # Açıklama
                self.ui_personel_sayfasi.request_table.setItem(row_idx, 5, QTableWidgetItem(req[5])) # Öncelik
                self.ui_personel_sayfasi.request_table.setItem(row_idx, 6, QTableWidgetItem(req[6])) # Durum
                self.ui_personel_sayfasi.request_table.setItem(row_idx, 7, QTableWidgetItem(str(req[7]))) # Oluşturma Tarihi
                self.ui_personel_sayfasi.request_table.setItem(row_idx, 8, QTableWidgetItem(str(req[8]) if req[8] else "Yok")) # Çözüm Tarihi
                self.ui_personel_sayfasi.request_table.setItem(row_idx, 9, QTableWidgetItem(req[9] if req[9] else "Atanmadı")) # Çözen Personel Ad Soyad
        else:
            self.ui_personel_sayfasi.talep_sec_label.setText("Seçili Talep ID: Yok")
            QMessageBox.information(self, "Bilgi", "Hiç talep bulunamadı veya aramanızla eşleşen sonuç yok.")

    def handle_personnel_table_selection(self, row, column):
        selected_id_item = self.ui_personel_sayfasi.request_table.item(row, 0)
        if selected_id_item:
            self.selected_request_id = int(selected_id_item.text())
            self.ui_personel_sayfasi.talep_sec_label.setText(f"Seçili Talep ID: {self.selected_request_id}")
            # Seçili talebin mevcut durumunu combobox'a yansıt
            current_status = self.ui_personel_sayfasi.request_table.item(row, 6).text()
            self.ui_personel_sayfasi.update_status_combo.setCurrentText(current_status)
        else:
            self.selected_request_id = None
            self.ui_personel_sayfasi.talep_sec_label.setText("Seçili Talep ID: Yok")

    def handle_update_talep_durum(self):
        if self.selected_request_id is None:
            QMessageBox.warning(self, "Uyarı", "Lütfen güncellemek istediğiniz bir talep seçin.")
            return

        new_status = self.ui_personel_sayfasi.update_status_combo.currentText()
        update_query = ""
        params = ()

        if new_status == "Tamamlandı":
            # Eğer tamamlandı olarak işaretleniyorsa çözüm tarihini ve çözen personeli de kaydet
            cozum_tarihi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            update_query = """
            UPDATE destek_talep
            SET durum = %s, cozum_tarihi = %s, cozumu_yapan_id = %s
            WHERE id = %s
            """
            params = (new_status, cozum_tarihi, self.current_user_id, self.selected_request_id)
        else:
            # Diğer durumlar için sadece durumu güncelle, çözüm tarihi ve çözen kişiyi NULL yap
            update_query = """
            UPDATE destek_talep
            SET durum = %s, cozum_tarihi = NULL, cozumu_yapan_id = NULL
            WHERE id = %s
            """
            params = (new_status, self.selected_request_id)

        if self.db.execute_query(update_query, params):
            QMessageBox.information(self, "Başarılı", f"Talep ID: {self.selected_request_id} durumu '{new_status}' olarak güncellendi.")
            self.load_all_requests_personnel() # Listeyi yenile
            self.selected_request_id = None # Seçimi temizle
            self.ui_personel_sayfasi.talep_sec_label.setText("Seçili Talep ID: Yok")
        else:
            QMessageBox.critical(self, "Hata", "Talep durumu güncellenirken bir sorun oluştu.")

    def handle_delete_talep(self):
        if self.selected_request_id is None:
            QMessageBox.warning(self, "Uyarı", "Lütfen silmek istediğiniz bir talep seçin.")
            return

        reply = QMessageBox.question(self, 'Talebi Sil',
                                     f'ID {self.selected_request_id} olan talebi silmek istediğinizden emin misiniz?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            query = "DELETE FROM destek_talep WHERE id = %s"
            if self.db.execute_query(query, (self.selected_request_id,)):
                QMessageBox.information(self, "Başarılı", f"Talep ID: {self.selected_request_id} başarıyla silindi.")
                self.load_all_requests_personnel() # Listeyi yenile
                self.selected_request_id = None # Seçimi temizle
                self.ui_personel_sayfasi.talep_sec_label.setText("Seçili Talep ID: Yok")
            else:
                QMessageBox.critical(self, "Hata", "Talep silinirken bir sorun oluştu.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
