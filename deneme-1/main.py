import sys
import sqlite3
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QListWidget, QPushButton,
    QVBoxLayout, QHBoxLayout, QStackedWidget, QLabel, QLineEdit, QTextEdit,
    QDateEdit, QComboBox, QTableWidget, QTableWidgetItem, QFormLayout,
    QMessageBox, QInputDialog, QFrame, QSplitter, QTabWidget, QDialog, QDialogButtonBox
)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QPalette, QColor

class Gorev:
    def __init__(self, adi, sorumlu, durum, baslangic, bitis):
        self.adi = adi
        self.sorumlu = sorumlu
        self.durum = durum
        self.baslangic = baslangic
        self.bitis = bitis

class Proje:
    def __init__(self, proje_adi):
        self.proje_adi = proje_adi
        self.gorevler = []

    def gorev_ekle(self, gorev):
        self.gorevler.append(gorev)

    def gorev_durum_istatistikleri(self):
        durumlar = {}
        for gorev in self.gorevler:
            if gorev.durum in durumlar:
                durumlar[gorev.durum] += 1
            else:
                durumlar[gorev.durum] = 1
        return durumlar

class ProjeTakipApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Proje Takip ve Raporlama Sistemi")
        self.resize(1200, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            QWidget {
                background-color: #f0f2f5;
                color: #1a1a1a;
            }
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
            QLineEdit, QTextEdit, QDateEdit, QComboBox {
                padding: 5px;
                border: 1px solid #dcdde1;
                border-radius: 4px;
                background-color: white;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #dcdde1;
                border-radius: 4px;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #9b59b6;
                color: white;
            }
            QListWidget {
                background-color: white;
                border: 1px solid #dcdde1;
                border-radius: 4px;
            }
            QListWidget::item {
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #9b59b6;
                color: white;
            }
            QStackedWidget {
                background-color: #e8eaf6;
            }
            QFrame {
                background-color: #e8eaf6;
            }
            QLabel {
                color: #1a1a1a;
            }
        """)

        self.connection = sqlite3.connect('proje_takip.db')
        self._create_tables()
        self._init_ui()
        self.load_projeler()

    def _create_tables(self):
        cursor = self.connection.cursor()

        # Kullanıcılar tablosu
        cursor.execute('''CREATE TABLE IF NOT EXISTS kullanicilar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad_soyad TEXT NOT NULL,
            eposta TEXT UNIQUE,
            rol TEXT,
            departman TEXT,
            telefon TEXT
        )''')

        # Projeler tablosu
        cursor.execute('''CREATE TABLE IF NOT EXISTS projeler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad TEXT NOT NULL,
            aciklama TEXT,
            baslangic_tarihi TEXT,
            bitis_tarihi TEXT,
            durum TEXT,
            oncelik TEXT,
            butce REAL,
            ilerleme INTEGER,
            proje_yoneticisi_id INTEGER,
            FOREIGN KEY (proje_yoneticisi_id) REFERENCES kullanicilar (id)
        )''')

        # Görevler tablosu
        cursor.execute('''CREATE TABLE IF NOT EXISTS gorevler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proje_id INTEGER,
            baslik TEXT NOT NULL,
            aciklama TEXT,
            baslangic_tarihi TEXT,
            bitis_tarihi TEXT,
            durum TEXT,
            oncelik TEXT,
            sorumlu_id INTEGER,
            tahmini_sure INTEGER,
            gerceklesen_sure INTEGER,
            FOREIGN KEY (proje_id) REFERENCES projeler (id),
            FOREIGN KEY (sorumlu_id) REFERENCES kullanicilar (id)
        )''')

        # Raporlar tablosu
        cursor.execute('''CREATE TABLE IF NOT EXISTS raporlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proje_id INTEGER,
            gorev_id INTEGER,
            baslik TEXT NOT NULL,
            icerik TEXT,
            rapor_tarihi TEXT,
            rapor_tipi TEXT,
            olusturan_id INTEGER,
            FOREIGN KEY (proje_id) REFERENCES projeler (id),
            FOREIGN KEY (gorev_id) REFERENCES gorevler (id),
            FOREIGN KEY (olusturan_id) REFERENCES kullanicilar (id)
        )''')

        # Riskler tablosu
        cursor.execute('''CREATE TABLE IF NOT EXISTS riskler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proje_id INTEGER,
            baslik TEXT NOT NULL,
            aciklama TEXT,
            etki_seviyesi TEXT,
            olasilik TEXT,
            onlem TEXT,
            durum TEXT,
            FOREIGN KEY (proje_id) REFERENCES projeler (id)
        )''')

        # Örnek verileri ekle
        try:
            # Kullanıcılar
            kullanicilar = [
                ('Ahmet Yılmaz', 'ahmet@firma.com', 'Proje Yöneticisi', 'Yönetim', '555-0001'),
                ('Ayşe Demir', 'ayse@firma.com', 'Takım Lideri', 'Yazılım', '555-0002'),
                ('Mehmet Kaya', 'mehmet@firma.com', 'Geliştirici', 'Yazılım', '555-0003'),
                ('Zeynep Şahin', 'zeynep@firma.com', 'Tasarımcı', 'Tasarım', '555-0004'),
                ('Can Öz', 'can@firma.com', 'Test Uzmanı', 'Kalite', '555-0005')
            ]
            cursor.executemany('''INSERT OR IGNORE INTO kullanicilar 
                (ad_soyad, eposta, rol, departman, telefon) VALUES (?, ?, ?, ?, ?)''', kullanicilar)

            # Projeler
            projeler = [
                ('E-Ticaret Platformu', 'Online alışveriş platformu geliştirme', '2024-01-01', '2024-06-30', 'Devam Ediyor', 'Yüksek', 500000, 45, 1),
                ('Mobil Uygulama', 'iOS ve Android uygulaması geliştirme', '2024-02-01', '2024-07-31', 'Planlandı', 'Orta', 300000, 0, 2),
                ('Web Sitesi Yenileme', 'Kurumsal web sitesi yenileme projesi', '2024-01-15', '2024-04-15', 'Devam Ediyor', 'Yüksek', 200000, 60, 1),
                ('Veri Analizi Projesi', 'Büyük veri analizi ve raporlama', '2024-03-01', '2024-08-31', 'Planlandı', 'Düşük', 400000, 0, 2),
                ('Güvenlik Güncellemesi', 'Sistem güvenlik güncellemeleri', '2024-02-15', '2024-05-15', 'Devam Ediyor', 'Yüksek', 150000, 30, 1)
            ]
            cursor.executemany('''INSERT OR IGNORE INTO projeler 
                (ad, aciklama, baslangic_tarihi, bitis_tarihi, durum, oncelik, butce, ilerleme, proje_yoneticisi_id) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', projeler)

            # Görevler
            gorevler = [
                (1, 'Veritabanı Tasarımı', 'Veritabanı şeması oluşturma', '2024-01-01', '2024-01-15', 'Tamamlandı', 'Yüksek', 1, 40, 35),
                (1, 'Frontend Geliştirme', 'Kullanıcı arayüzü geliştirme', '2024-01-16', '2024-02-15', 'Devam Ediyor', 'Yüksek', 2, 60, 45),
                (1, 'Backend API', 'REST API geliştirme', '2024-01-16', '2024-02-28', 'Devam Ediyor', 'Yüksek', 3, 80, 50),
                (1, 'Ödeme Sistemi', 'Ödeme altyapısı entegrasyonu', '2024-02-16', '2024-03-15', 'Planlandı', 'Yüksek', 2, 0, 0),
                (2, 'UI/UX Tasarımı', 'Mobil uygulama tasarımı', '2024-02-01', '2024-02-28', 'Planlandı', 'Orta', 4, 0, 0),
                (2, 'iOS Geliştirme', 'iOS uygulaması geliştirme', '2024-03-01', '2024-05-31', 'Planlandı', 'Yüksek', 3, 0, 0),
                (2, 'Android Geliştirme', 'Android uygulaması geliştirme', '2024-03-01', '2024-05-31', 'Planlandı', 'Yüksek', 3, 0, 0),
                (3, 'İçerik Hazırlama', 'Web sitesi içeriklerinin hazırlanması', '2024-01-15', '2024-02-15', 'Tamamlandı', 'Orta', 1, 40, 40),
                (3, 'Tasarım Uygulama', 'Yeni tasarımın uygulanması', '2024-02-16', '2024-03-15', 'Devam Ediyor', 'Yüksek', 4, 70, 60),
                (3, 'Test ve Optimizasyon', 'Performans testleri ve optimizasyon', '2024-03-16', '2024-04-15', 'Planlandı', 'Orta', 5, 0, 0),
                (4, 'Veri Toplama', 'Veri kaynaklarının belirlenmesi', '2024-03-01', '2024-03-15', 'Planlandı', 'Orta', 2, 0, 0),
                (4, 'Analiz Altyapısı', 'Analiz sisteminin kurulması', '2024-03-16', '2024-04-30', 'Planlandı', 'Yüksek', 3, 0, 0),
                (4, 'Raporlama Sistemi', 'Raporlama arayüzü geliştirme', '2024-05-01', '2024-06-30', 'Planlandı', 'Orta', 2, 0, 0),
                (5, 'Güvenlik Analizi', 'Mevcut sistem güvenlik analizi', '2024-02-15', '2024-03-15', 'Devam Ediyor', 'Yüksek', 5, 50, 40),
                (5, 'Güncelleme Planı', 'Güncelleme planının hazırlanması', '2024-03-16', '2024-04-15', 'Planlandı', 'Yüksek', 1, 0, 0)
            ]
            cursor.executemany('''INSERT OR IGNORE INTO gorevler 
                (proje_id, baslik, aciklama, baslangic_tarihi, bitis_tarihi, durum, oncelik, sorumlu_id, tahmini_sure, gerceklesen_sure) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', gorevler)

            # Raporlar
            raporlar = [
                (1, 1, 'Veritabanı Tasarımı Tamamlandı', 'Veritabanı şeması başarıyla oluşturuldu ve test edildi.', '2024-01-15', 'İlerleme', 1),
                (1, 2, 'Frontend Geliştirme Durumu', 'Ana sayfa ve ürün listeleme sayfaları tamamlandı.', '2024-02-01', 'İlerleme', 2),
                (1, 3, 'API Geliştirme Raporu', 'Temel API endpointleri tamamlandı.', '2024-02-15', 'İlerleme', 3),
                (3, 8, 'İçerik Hazırlama Tamamlandı', 'Tüm içerikler hazırlandı ve onaylandı.', '2024-02-15', 'İlerleme', 1),
                (3, 9, 'Tasarım Uygulama Durumu', 'Ana sayfa ve iletişim sayfası tasarımları uygulandı.', '2024-03-01', 'İlerleme', 4),
                (5, 14, 'Güvenlik Analizi Raporu', 'Kritik güvenlik açıkları tespit edildi.', '2024-03-01', 'Risk', 5)
            ]
            cursor.executemany('''INSERT OR IGNORE INTO raporlar 
                (proje_id, gorev_id, baslik, icerik, rapor_tarihi, rapor_tipi, olusturan_id) 
                VALUES (?, ?, ?, ?, ?, ?, ?)''', raporlar)

            # Riskler
            riskler = [
                (1, 'Ödeme Sistemi Entegrasyonu', 'Ödeme sağlayıcısı ile entegrasyon gecikmesi', 'Yüksek', 'Orta', 'Alternatif sağlayıcı araştırması yapılacak', 'Aktif'),
                (1, 'Performans Sorunları', 'Yüksek trafikte performans düşüşü', 'Orta', 'Düşük', 'Önbellek sistemi kurulacak', 'Aktif'),
                (2, 'App Store Onayı', 'Apple App Store onay süreci gecikmesi', 'Yüksek', 'Orta', 'Erken test sürecine başlanacak', 'Aktif'),
                (3, 'İçerik Gecikmesi', 'İçerik sağlayıcılardan gecikme', 'Orta', 'Yüksek', 'İçerik takvimi güncellendi', 'Çözüldü'),
                (4, 'Veri Kalitesi', 'Kaynak verilerde tutarsızlık', 'Yüksek', 'Orta', 'Veri doğrulama sistemi geliştirilecek', 'Aktif'),
                (5, 'Sistem Kesintisi', 'Güncelleme sırasında olası kesinti', 'Yüksek', 'Düşük', 'Yedekli geçiş planı hazırlandı', 'Aktif')
            ]
            cursor.executemany('''INSERT OR IGNORE INTO riskler 
                (proje_id, baslik, aciklama, etki_seviyesi, olasilik, onlem, durum) 
                VALUES (?, ?, ?, ?, ?, ?, ?)''', riskler)

            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Veritabanı hatası: {e}")

    def _init_ui(self):
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Sol menü
        sol_menu = QFrame()
        sol_menu.setMaximumWidth(250)
        sol_menu.setMinimumWidth(250)
        sol_menu.setStyleSheet("""
            QFrame {
                background-color: #5c6bc0;
                border-radius: 4px;
            }
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton {
                text-align: left;
                padding: 10px;
                border: none;
                color: white;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #3949ab;
            }
            QListWidget {
                background-color: transparent;
                border: none;
                color: white;
            }
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:selected {
                background-color: #3949ab;
            }
        """)

        sol_menu_layout = QVBoxLayout()
        sol_menu_layout.setContentsMargins(0, 0, 0, 0)
        sol_menu_layout.setSpacing(0)

        # Logo veya başlık
        baslik = QLabel("Proje Takip\nve Raporlama")
        baslik.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sol_menu_layout.addWidget(baslik)

        # Proje listesi
        self.proje_listesi = QListWidget()
        self.proje_listesi.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
                color: white;
            }
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:selected {
                background-color: #3949ab;
            }
        """)
        sol_menu_layout.addWidget(self.proje_listesi)

        # Menü butonları
        self.btn_yeni_proje = QPushButton("Yeni Proje")
        self.btn_yeni_gorev = QPushButton("Yeni Görev")
        self.btn_raporlar = QPushButton("Raporlar")
        self.btn_riskler = QPushButton("Riskler")
        self.btn_grafikler = QPushButton("Grafikler")
        self.btn_veritabani = QPushButton("Veritabanı")
        self.btn_ayarlar = QPushButton("Ayarlar")

        sol_menu_layout.addWidget(self.btn_yeni_proje)
        sol_menu_layout.addWidget(self.btn_yeni_gorev)
        sol_menu_layout.addWidget(self.btn_raporlar)
        sol_menu_layout.addWidget(self.btn_riskler)
        sol_menu_layout.addWidget(self.btn_grafikler)
        sol_menu_layout.addWidget(self.btn_veritabani)
        sol_menu_layout.addWidget(self.btn_ayarlar)
        sol_menu_layout.addStretch()

        sol_menu.setLayout(sol_menu_layout)

        # Ana içerik alanı
        self.stacked_widget = QStackedWidget()

        # Proje detay sayfası
        self.proje_detay_widget = QWidget()
        self._init_proje_detay_ui()
        self.stacked_widget.addWidget(self.proje_detay_widget)

        # Raporlar sayfası
        self.raporlar_widget = QWidget()
        self._init_raporlar_ui()
        self.stacked_widget.addWidget(self.raporlar_widget)

        # Riskler sayfası
        self.riskler_widget = QWidget()
        self._init_riskler_ui()
        self.stacked_widget.addWidget(self.riskler_widget)

        # Grafikler sayfası
        self.grafikler_widget = QWidget()
        self._init_grafikler_ui()
        self.stacked_widget.addWidget(self.grafikler_widget)

        # Ayarlar sayfası
        self.ayarlar_widget = QWidget()
        self._init_ayarlar_ui()
        self.stacked_widget.addWidget(self.ayarlar_widget)

        # Veritabanı görüntüleme sayfası
        self.veritabani_widget = QWidget()
        self._init_veritabani_ui()
        self.stacked_widget.addWidget(self.veritabani_widget)

        main_layout.addWidget(sol_menu)
        main_layout.addWidget(self.stacked_widget)

        # Sinyal bağlantıları
        self.btn_yeni_proje.clicked.connect(self.yeni_proje_ekle)
        self.btn_yeni_gorev.clicked.connect(self.yeni_gorev_ekle)
        self.btn_raporlar.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.raporlar_widget))
        self.btn_riskler.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.riskler_widget))
        self.btn_grafikler.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.grafikler_widget))
        self.btn_ayarlar.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.ayarlar_widget))
        self.btn_veritabani.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.veritabani_widget))
        self.proje_listesi.currentRowChanged.connect(self.proje_secildi)

    def _init_proje_detay_ui(self):
        layout = QVBoxLayout()
        
        # Üst bilgi kartı
        info_card = QFrame()
        info_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 4px;
                padding: 15px;
            }
        """)
        info_layout = QFormLayout()
        
        self.le_proje_adi = QLineEdit()
        self.te_proje_aciklama = QTextEdit()
        self.te_proje_aciklama.setMaximumHeight(100)
        self.de_baslangic = QDateEdit()
        self.de_baslangic.setCalendarPopup(True)
        self.de_bitis = QDateEdit()
        self.de_bitis.setCalendarPopup(True)
        self.cb_durum = QComboBox()
        self.cb_durum.addItems(["Planlandı", "Devam Ediyor", "Tamamlandı", "Askıya Alındı", "İptal Edildi"])
        self.cb_oncelik = QComboBox()
        self.cb_oncelik.addItems(["Düşük", "Orta", "Yüksek", "Acil"])
        self.le_butce = QLineEdit()
        self.le_butce.setPlaceholderText("TL")
        
        info_layout.addRow("Proje Adı:", self.le_proje_adi)
        info_layout.addRow("Açıklama:", self.te_proje_aciklama)
        info_layout.addRow("Başlangıç:", self.de_baslangic)
        info_layout.addRow("Bitiş:", self.de_bitis)
        info_layout.addRow("Durum:", self.cb_durum)
        info_layout.addRow("Öncelik:", self.cb_oncelik)
        info_layout.addRow("Bütçe:", self.le_butce)
        
        info_card.setLayout(info_layout)
        layout.addWidget(info_card)

        # Görevler kartı
        tasks_card = QFrame()
        tasks_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 4px;
                padding: 15px;
            }
        """)
        tasks_layout = QVBoxLayout()
        
        tasks_header = QHBoxLayout()
        tasks_header.addWidget(QLabel("Görevler"))
        self.btn_gorev_duzenle = QPushButton("Görevi Düzenle")
        self.btn_gorev_sil = QPushButton("Görevi Sil")
        tasks_header.addWidget(self.btn_gorev_duzenle)
        tasks_header.addWidget(self.btn_gorev_sil)
        tasks_layout.addLayout(tasks_header)

        self.gorev_tablosu = QTableWidget(0, 6)
        self.gorev_tablosu.setHorizontalHeaderLabels([
            "ID", "Görev Adı", "Sorumlu", "Başlangıç", "Bitiş", "Durum", "İlerleme"
        ])
        self.gorev_tablosu.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.gorev_tablosu.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        tasks_layout.addWidget(self.gorev_tablosu)
        
        tasks_card.setLayout(tasks_layout)
        layout.addWidget(tasks_card)

        # Kaydet butonu
        self.btn_kaydet = QPushButton("Değişiklikleri Kaydet")
        self.btn_kaydet.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        layout.addWidget(self.btn_kaydet, alignment=Qt.AlignmentFlag.AlignRight)

        self.proje_detay_widget.setLayout(layout)

        # Sinyal bağlantıları
        self.btn_gorev_duzenle.clicked.connect(lambda: self.gorev_duzenle(self.gorev_tablosu.currentRow()))
        self.btn_gorev_sil.clicked.connect(self.gorev_sil)
        self.btn_kaydet.clicked.connect(self.proje_kaydet)

    def _init_raporlar_ui(self):
        layout = QVBoxLayout()
        
        # Rapor seçenekleri
        form_layout = QFormLayout()
        self.cb_rapor_tipi = QComboBox()
        self.cb_rapor_tipi.addItems([
            "Proje Durumu Özeti",
            "Görev İlerleme Raporu",
            "Risk Analizi",
            "Bütçe Durumu",
            "Takım Performansı"
        ])
        form_layout.addRow("Rapor Tipi:", self.cb_rapor_tipi)
        
        self.btn_rapor_olustur = QPushButton("Rapor Oluştur")
        form_layout.addRow("", self.btn_rapor_olustur)
        
        layout.addLayout(form_layout)
        
        # Rapor görüntüleme alanı
        self.te_rapor = QTextEdit()
        self.te_rapor.setReadOnly(True)
        layout.addWidget(self.te_rapor)
        
        self.raporlar_widget.setLayout(layout)
        
        # Sinyal bağlantısı
        self.btn_rapor_olustur.clicked.connect(self.rapor_olustur)

    def _init_riskler_ui(self):
        layout = QVBoxLayout()
        
        # Risk yönetimi başlığı
        header = QHBoxLayout()
        header.addWidget(QLabel("Risk Yönetimi"))
        self.btn_yeni_risk = QPushButton("Yeni Risk Ekle")
        header.addWidget(self.btn_yeni_risk)
        layout.addLayout(header)
        
        # Risk tablosu
        self.risk_tablosu = QTableWidget(0, 6)
        self.risk_tablosu.setHorizontalHeaderLabels([
            "Risk", "Etki", "Olasılık", "Önlem", "Durum", "İşlemler"
        ])
        layout.addWidget(self.risk_tablosu)
        
        self.riskler_widget.setLayout(layout)
        
        # Sinyal bağlantısı
        self.btn_yeni_risk.clicked.connect(self.yeni_risk_ekle)

    def _init_grafikler_ui(self):
        layout = QVBoxLayout()
        
        # Grafik seçenekleri
        form_layout = QFormLayout()
        self.cb_grafik_tipi = QComboBox()
        self.cb_grafik_tipi.addItems([
            "Gantt Şeması",
            "Görev Durumu Pasta Grafiği"
        ])
        form_layout.addRow("Grafik Tipi:", self.cb_grafik_tipi)
        
        self.btn_grafik_olustur = QPushButton("Grafik Oluştur")
        form_layout.addRow("", self.btn_grafik_olustur)
        
        layout.addLayout(form_layout)
        self.grafikler_widget.setLayout(layout)
        
        # Sinyal bağlantısı
        self.btn_grafik_olustur.clicked.connect(self.grafik_olustur)

    def _init_ayarlar_ui(self):
        layout = QVBoxLayout()
        
        # Kullanıcı yönetimi
        form_layout = QFormLayout()
        self.le_kullanici_adi = QLineEdit()
        self.le_eposta = QLineEdit()
        self.cb_rol = QComboBox()
        self.cb_rol.addItems(["Proje Yöneticisi", "Takım Lideri", "Geliştirici", "Tasarımcı", "Test Uzmanı"])
        self.le_departman = QLineEdit()
        self.le_telefon = QLineEdit()
        
        form_layout.addRow("Ad Soyad:", self.le_kullanici_adi)
        form_layout.addRow("E-posta:", self.le_eposta)
        form_layout.addRow("Rol:", self.cb_rol)
        form_layout.addRow("Departman:", self.le_departman)
        form_layout.addRow("Telefon:", self.le_telefon)
        
        self.btn_kullanici_ekle = QPushButton("Kullanıcı Ekle")
        form_layout.addRow("", self.btn_kullanici_ekle)
        
        layout.addLayout(form_layout)
        self.ayarlar_widget.setLayout(layout)
        
        # Sinyal bağlantısı
        self.btn_kullanici_ekle.clicked.connect(self.kullanici_ekle)

    def _init_veritabani_ui(self):
        layout = QVBoxLayout()
        
        # Tab widget oluştur
        tab_widget = QTabWidget()
        
        # Kullanıcılar tablosu
        kullanicilar_tab = QWidget()
        kullanicilar_layout = QVBoxLayout()
        self.kullanicilar_tablosu = QTableWidget()
        kullanicilar_layout.addWidget(self.kullanicilar_tablosu)
        kullanicilar_tab.setLayout(kullanicilar_layout)
        
        # Projeler tablosu
        projeler_tab = QWidget()
        projeler_layout = QVBoxLayout()
        self.projeler_tablosu = QTableWidget()
        projeler_layout.addWidget(self.projeler_tablosu)
        projeler_tab.setLayout(projeler_layout)
        
        # Görevler tablosu
        gorevler_tab = QWidget()
        gorevler_layout = QVBoxLayout()
        self.gorevler_tablosu = QTableWidget()
        gorevler_layout.addWidget(self.gorevler_tablosu)
        gorevler_tab.setLayout(gorevler_layout)
        
        # Raporlar tablosu
        raporlar_tab = QWidget()
        raporlar_layout = QVBoxLayout()
        self.raporlar_tablosu = QTableWidget()
        raporlar_layout.addWidget(self.raporlar_tablosu)
        raporlar_tab.setLayout(raporlar_layout)
        
        # Riskler tablosu
        riskler_tab = QWidget()
        riskler_layout = QVBoxLayout()
        self.riskler_tablosu = QTableWidget()
        riskler_layout.addWidget(self.riskler_tablosu)
        riskler_tab.setLayout(riskler_layout)
        
        # Tabları ekle
        tab_widget.addTab(kullanicilar_tab, "Kullanıcılar")
        tab_widget.addTab(projeler_tab, "Projeler")
        tab_widget.addTab(gorevler_tab, "Görevler")
        tab_widget.addTab(raporlar_tab, "Raporlar")
        tab_widget.addTab(riskler_tab, "Riskler")
        
        layout.addWidget(tab_widget)
        
        # Yenile butonu
        refresh_layout = QHBoxLayout()
        self.btn_veritabani_yenile = QPushButton("Yenile")
        refresh_layout.addStretch()
        refresh_layout.addWidget(self.btn_veritabani_yenile)
        layout.addLayout(refresh_layout)
        
        self.veritabani_widget.setLayout(layout)
        
        # Sinyal bağlantıları
        self.btn_veritabani_yenile.clicked.connect(self.veritabani_yenile)
        tab_widget.currentChanged.connect(self.veritabani_yenile)
        self.btn_veritabani.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.veritabani_widget))

    def veritabani_yenile(self):
        try:
            cursor = self.connection.cursor()
            
            # Kullanıcılar tablosunu güncelle
            cursor.execute("SELECT * FROM kullanicilar")
            kullanicilar = cursor.fetchall()
            self.kullanicilar_tablosu.setRowCount(len(kullanicilar))
            self.kullanicilar_tablosu.setColumnCount(6)
            self.kullanicilar_tablosu.setHorizontalHeaderLabels([
                "ID", "Ad Soyad", "E-posta", "Rol", "Departman", "Telefon"
            ])
            for row, kullanici in enumerate(kullanicilar):
                for col, veri in enumerate(kullanici):
                    self.kullanicilar_tablosu.setItem(row, col, QTableWidgetItem(str(veri)))
            
            # Projeler tablosunu güncelle
            cursor.execute("SELECT * FROM projeler")
            projeler = cursor.fetchall()
            self.projeler_tablosu.setRowCount(len(projeler))
            self.projeler_tablosu.setColumnCount(9)
            self.projeler_tablosu.setHorizontalHeaderLabels([
                "ID", "Proje Adı", "Açıklama", "Başlangıç Tarihi", 
                "Bitiş Tarihi", "Durum", "Öncelik", "Bütçe", "İlerleme"
            ])
            for row, proje in enumerate(projeler):
                for col, veri in enumerate(proje):
                    self.projeler_tablosu.setItem(row, col, QTableWidgetItem(str(veri)))
            
            # Görevler tablosunu güncelle
            cursor.execute("SELECT * FROM gorevler")
            gorevler = cursor.fetchall()
            self.gorevler_tablosu.setRowCount(len(gorevler))
            self.gorevler_tablosu.setColumnCount(11)
            self.gorevler_tablosu.setHorizontalHeaderLabels([
                "ID", "Proje ID", "Başlık", "Açıklama", "Başlangıç Tarihi", 
                "Bitiş Tarihi", "Durum", "Öncelik", "Sorumlu ID", 
                "Tahmini Süre", "Gerçekleşen Süre"
            ])
            for row, gorev in enumerate(gorevler):
                for col, veri in enumerate(gorev):
                    self.gorevler_tablosu.setItem(row, col, QTableWidgetItem(str(veri)))
            
            # Raporlar tablosunu güncelle
            cursor.execute("SELECT * FROM raporlar")
            raporlar = cursor.fetchall()
            self.raporlar_tablosu.setRowCount(len(raporlar))
            self.raporlar_tablosu.setColumnCount(8)
            self.raporlar_tablosu.setHorizontalHeaderLabels([
                "ID", "Proje ID", "Görev ID", "Başlık", "İçerik", 
                "Rapor Tarihi", "Rapor Tipi", "Oluşturan ID"
            ])
            for row, rapor in enumerate(raporlar):
                for col, veri in enumerate(rapor):
                    self.raporlar_tablosu.setItem(row, col, QTableWidgetItem(str(veri)))
            
            # Riskler tablosunu güncelle
            cursor.execute("SELECT * FROM riskler")
            riskler = cursor.fetchall()
            self.riskler_tablosu.setRowCount(len(riskler))
            self.riskler_tablosu.setColumnCount(8)
            self.riskler_tablosu.setHorizontalHeaderLabels([
                "ID", "Proje ID", "Başlık", "Açıklama", "Etki Seviyesi",
                "Olasılık", "Önlem", "Durum"
            ])
            for row, risk in enumerate(riskler):
                for col, veri in enumerate(risk):
                    self.riskler_tablosu.setItem(row, col, QTableWidgetItem(str(veri)))
            
            # Sütun genişliklerini ayarla
            for tablo in [self.kullanicilar_tablosu, self.projeler_tablosu, 
                         self.gorevler_tablosu, self.raporlar_tablosu,
                         self.riskler_tablosu]:
                tablo.resizeColumnsToContents()
                tablo.horizontalHeader().setStretchLastSection(True)

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Veritabanı Hatası", f"Veriler yüklenirken hata oluştu: {str(e)}")

    def load_projeler(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT ad FROM projeler")
        projeler = cursor.fetchall()
        self.proje_listesi.clear()
        for proje in projeler:
            self.proje_listesi.addItem(proje[0])

    def yeni_proje_ekle(self):
        proje_adi, ok = QInputDialog.getText(self, "Yeni Proje", "Proje Adı:")
        if ok and proje_adi.strip():
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO projeler (ad, aciklama, baslangic_tarihi, bitis_tarihi, durum, oncelik, butce, ilerleme) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (proje_adi.strip(), "Yeni proje açıklaması", 
                 QDate.currentDate().toString("yyyy-MM-dd"),
                 QDate.currentDate().addDays(30).toString("yyyy-MM-dd"),
                 "Planlandı", "Orta", 0.0, 0))
            self.connection.commit()
            self.load_projeler()
            QMessageBox.information(self, "Başarılı", f"'{proje_adi}' projesi eklendi.")
        else:
            QMessageBox.warning(self, "Hata", "Geçerli bir proje adı giriniz.")

    def proje_secildi(self, index):
        if index < 0:
            return
            
        proje_adi = self.proje_listesi.item(index).text()
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM projeler WHERE ad = ?", (proje_adi,))
        proje = cursor.fetchone()
        
        if proje:
            self.le_proje_adi.setText(proje[1])  # ad
            self.te_proje_aciklama.setPlainText(proje[2])  # aciklama
            self.de_baslangic.setDate(QDate.fromString(proje[3], "yyyy-MM-dd"))  # baslangic_tarihi
            self.de_bitis.setDate(QDate.fromString(proje[4], "yyyy-MM-dd"))  # bitis_tarihi
            self.cb_durum.setCurrentText(proje[5])  # durum
            self.cb_oncelik.setCurrentText(proje[6])  # oncelik
            self.le_butce.setText(str(proje[7]))  # butce
            
            # Görevleri yükle
            cursor.execute("SELECT * FROM gorevler WHERE proje_id = ?", (proje[0],))
            gorevler = cursor.fetchall()
            self.gorev_tablosu.setRowCount(len(gorevler))
            for row, gorev in enumerate(gorevler):
                self.gorev_tablosu.setItem(row, 0, QTableWidgetItem(gorev[2]))  # baslik
                self.gorev_tablosu.setItem(row, 1, QTableWidgetItem(gorev[8] if len(gorev) > 8 else ""))  # sorumlu
                self.gorev_tablosu.setItem(row, 2, QTableWidgetItem(gorev[4]))  # baslangic_tarihi
                self.gorev_tablosu.setItem(row, 3, QTableWidgetItem(gorev[5]))  # bitis_tarihi
                self.gorev_tablosu.setItem(row, 4, QTableWidgetItem(gorev[6]))  # durum
                self.gorev_tablosu.setItem(row, 5, QTableWidgetItem(str(gorev[10] if len(gorev) > 10 else 0)))  # ilerleme

    def yeni_gorev_ekle(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Yeni Görev Ekle")
        dialog.setMinimumWidth(500)
        layout = QFormLayout()

        # Görev başlığı
        le_baslik = QLineEdit()
        layout.addRow("Görev Başlığı:", le_baslik)

        # Görev açıklaması
        te_aciklama = QTextEdit()
        te_aciklama.setMaximumHeight(100)
        layout.addRow("Açıklama:", te_aciklama)

        # Başlangıç tarihi
        de_baslangic = QDateEdit()
        de_baslangic.setCalendarPopup(True)
        de_baslangic.setDate(QDate.currentDate())
        layout.addRow("Başlangıç Tarihi:", de_baslangic)

        # Bitiş tarihi
        de_bitis = QDateEdit()
        de_bitis.setCalendarPopup(True)
        de_bitis.setDate(QDate.currentDate().addDays(7))
        layout.addRow("Bitiş Tarihi:", de_bitis)

        # Durum seçimi
        cb_durum = QComboBox()
        cb_durum.addItems(["Planlandı", "Devam Ediyor", "Tamamlandı", "Askıya Alındı"])
        layout.addRow("Durum:", cb_durum)

        # Öncelik seçimi
        cb_oncelik = QComboBox()
        cb_oncelik.addItems(["Düşük", "Orta", "Yüksek", "Acil"])
        layout.addRow("Öncelik:", cb_oncelik)

        # Sorumlu kişi seçimi
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, ad_soyad FROM kullanicilar")
        kullanicilar = cursor.fetchall()
        cb_sorumlu = QComboBox()
        for kullanici in kullanicilar:
            cb_sorumlu.addItem(kullanici[1], kullanici[0])  # Görünen metin ve ID
        layout.addRow("Sorumlu:", cb_sorumlu)

        # Tahmini süre
        le_tahmini_sure = QLineEdit()
        le_tahmini_sure.setPlaceholderText("Saat cinsinden")
        layout.addRow("Tahmini Süre:", le_tahmini_sure)

        # Butonlar
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addRow(button_box)

        dialog.setLayout(layout)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                # Seçili projenin ID'sini al
                current_row = self.proje_listesi.currentRow()
                if current_row < 0:
                    QMessageBox.warning(self, "Hata", "Lütfen önce bir proje seçin.")
                    return

                proje_adi = self.proje_listesi.item(current_row).text()
                cursor.execute("SELECT id FROM projeler WHERE ad = ?", (proje_adi,))
                proje_id = cursor.fetchone()[0]

                # Görevi veritabanına ekle
                cursor.execute("""
                    INSERT INTO gorevler (
                        proje_id, baslik, aciklama, baslangic_tarihi, 
                        bitis_tarihi, durum, oncelik, sorumlu_id, 
                        tahmini_sure, gerceklesen_sure
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    proje_id,
                    le_baslik.text(),
                    te_aciklama.toPlainText(),
                    de_baslangic.date().toString("yyyy-MM-dd"),
                    de_bitis.date().toString("yyyy-MM-dd"),
                    cb_durum.currentText(),
                    cb_oncelik.currentText(),
                    cb_sorumlu.currentData(),  # Seçili kullanıcının ID'si
                    float(le_tahmini_sure.text() or 0),
                    0  # Başlangıçta gerçekleşen süre 0
                ))
                self.connection.commit()

                # Tabloyu güncelle
                self.proje_secildi(current_row)
                QMessageBox.information(self, "Başarılı", "Görev başarıyla eklendi.")

            except sqlite3.Error as e:
                QMessageBox.critical(self, "Veritabanı Hatası", f"Görev eklenirken hata oluştu: {str(e)}")
            except ValueError:
                QMessageBox.warning(self, "Hata", "Lütfen tahmini süreyi sayısal bir değer olarak girin.")

    def gorev_duzenle(self, row):
        if row < 0:
            return

        # Seçili görevin verilerini al
        gorev_id = self.gorev_tablosu.item(row, 0).text()
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM gorevler WHERE id = ?", (gorev_id,))
        gorev = cursor.fetchone()

        if not gorev:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Görev Düzenle")
        dialog.setMinimumWidth(500)
        layout = QFormLayout()

        # Görev başlığı
        le_baslik = QLineEdit(gorev[2])  # baslik
        layout.addRow("Görev Başlığı:", le_baslik)

        # Görev açıklaması
        te_aciklama = QTextEdit()
        te_aciklama.setPlainText(gorev[3])  # aciklama
        te_aciklama.setMaximumHeight(100)
        layout.addRow("Açıklama:", te_aciklama)

        # Başlangıç tarihi
        de_baslangic = QDateEdit()
        de_baslangic.setCalendarPopup(True)
        de_baslangic.setDate(QDate.fromString(gorev[4], "yyyy-MM-dd"))  # baslangic_tarihi
        layout.addRow("Başlangıç Tarihi:", de_baslangic)

        # Bitiş tarihi
        de_bitis = QDateEdit()
        de_bitis.setCalendarPopup(True)
        de_bitis.setDate(QDate.fromString(gorev[5], "yyyy-MM-dd"))  # bitis_tarihi
        layout.addRow("Bitiş Tarihi:", de_bitis)

        # Durum seçimi
        cb_durum = QComboBox()
        cb_durum.addItems(["Planlandı", "Devam Ediyor", "Tamamlandı", "Askıya Alındı"])
        cb_durum.setCurrentText(gorev[6])  # durum
        layout.addRow("Durum:", cb_durum)

        # Öncelik seçimi
        cb_oncelik = QComboBox()
        cb_oncelik.addItems(["Düşük", "Orta", "Yüksek", "Acil"])
        cb_oncelik.setCurrentText(gorev[7])  # oncelik
        layout.addRow("Öncelik:", cb_oncelik)

        # Sorumlu kişi seçimi
        cursor.execute("SELECT id, ad_soyad FROM kullanicilar")
        kullanicilar = cursor.fetchall()
        cb_sorumlu = QComboBox()
        for kullanici in kullanicilar:
            cb_sorumlu.addItem(kullanici[1], kullanici[0])
            if kullanici[0] == gorev[8]:  # sorumlu_id
                cb_sorumlu.setCurrentIndex(cb_sorumlu.count() - 1)
        layout.addRow("Sorumlu:", cb_sorumlu)

        # Tahmini süre
        le_tahmini_sure = QLineEdit(str(gorev[9]))  # tahmini_sure
        layout.addRow("Tahmini Süre:", le_tahmini_sure)

        # Gerçekleşen süre
        le_gerceklesen_sure = QLineEdit(str(gorev[10]))  # gerceklesen_sure
        layout.addRow("Gerçekleşen Süre:", le_gerceklesen_sure)

        # Butonlar
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addRow(button_box)

        dialog.setLayout(layout)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                cursor.execute("""
                    UPDATE gorevler 
                    SET baslik = ?, aciklama = ?, baslangic_tarihi = ?, 
                        bitis_tarihi = ?, durum = ?, oncelik = ?, 
                        sorumlu_id = ?, tahmini_sure = ?, gerceklesen_sure = ?
                    WHERE id = ?
                """, (
                    le_baslik.text(),
                    te_aciklama.toPlainText(),
                    de_baslangic.date().toString("yyyy-MM-dd"),
                    de_bitis.date().toString("yyyy-MM-dd"),
                    cb_durum.currentText(),
                    cb_oncelik.currentText(),
                    cb_sorumlu.currentData(),
                    float(le_tahmini_sure.text() or 0),
                    float(le_gerceklesen_sure.text() or 0),
                    gorev_id
                ))
                self.connection.commit()

                # Tabloyu güncelle
                current_row = self.proje_listesi.currentRow()
                self.proje_secildi(current_row)
                QMessageBox.information(self, "Başarılı", "Görev başarıyla güncellendi.")

            except sqlite3.Error as e:
                QMessageBox.critical(self, "Veritabanı Hatası", f"Görev güncellenirken hata oluştu: {str(e)}")
            except ValueError:
                QMessageBox.warning(self, "Hata", "Lütfen süreleri sayısal değerler olarak girin.")

    def gorev_sil(self):
        current_row = self.gorev_tablosu.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Hata", "Lütfen silinecek bir görev seçin.")
            return

        gorev_id = self.gorev_tablosu.item(current_row, 0).text()
        gorev_adi = self.gorev_tablosu.item(current_row, 1).text()

        reply = QMessageBox.question(
            self, 
            "Görevi Sil",
            f"'{gorev_adi}' görevini silmek istediğinizden emin misiniz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                cursor = self.connection.cursor()
                cursor.execute("DELETE FROM gorevler WHERE id = ?", (gorev_id,))
                self.connection.commit()

                # Tabloyu güncelle
                current_row = self.proje_listesi.currentRow()
                self.proje_secildi(current_row)
                QMessageBox.information(self, "Başarılı", "Görev başarıyla silindi.")

            except sqlite3.Error as e:
                QMessageBox.critical(self, "Veritabanı Hatası", f"Görev silinirken hata oluştu: {str(e)}")

    def proje_kaydet(self):
        current_row = self.proje_listesi.currentRow()
        if current_row >= 0:
            proje_adi = self.proje_listesi.item(current_row).text()
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE projeler 
                SET aciklama = ?, baslangic_tarihi = ?, bitis_tarihi = ?, 
                    durum = ?, oncelik = ?, butce = ?
                WHERE ad = ?
            """, (
                self.te_proje_aciklama.toPlainText(),
                self.de_baslangic.date().toString("yyyy-MM-dd"),
                self.de_bitis.date().toString("yyyy-MM-dd"),
                self.cb_durum.currentText(),
                self.cb_oncelik.currentText(),
                float(self.le_butce.text() or 0),
                proje_adi
            ))
            self.connection.commit()
            QMessageBox.information(self, "Başarılı", "Proje bilgileri güncellendi.")

    def rapor_olustur(self):
        rapor_tipi = self.cb_rapor_tipi.currentText()
        cursor = self.connection.cursor()
        
        if rapor_tipi == "Proje Durumu Özeti":
            cursor.execute("""
                SELECT durum, COUNT(*) as sayi
                FROM projeler
                GROUP BY durum
            """)
            sonuclar = cursor.fetchall()
            
            rapor = "PROJE DURUMU ÖZETİ\n"
            rapor += "=" * 30 + "\n\n"
            for durum, sayi in sonuclar:
                rapor += f"{durum}: {sayi} proje\n"
                
        elif rapor_tipi == "Görev İlerleme Raporu":
            cursor.execute("""
                SELECT p.ad, COUNT(g.id) as toplam_gorev,
                       SUM(CASE WHEN g.durum = 'Tamamlandı' THEN 1 ELSE 0 END) as tamamlanan
                FROM projeler p
                LEFT JOIN gorevler g ON p.id = g.proje_id
                GROUP BY p.id
            """)
            sonuclar = cursor.fetchall()
            
            rapor = "GÖREV İLERLEME RAPORU\n"
            rapor += "=" * 30 + "\n\n"
            for proje, toplam, tamamlanan in sonuclar:
                rapor += f"{proje}\n"
                rapor += f"  Toplam Görev: {toplam}\n"
                rapor += f"  Tamamlanan: {tamamlanan}\n"
                rapor += f"  İlerleme: {(tamamlanan/toplam*100 if toplam > 0 else 0):.1f}%\n\n"
                
        elif rapor_tipi == "Risk Analizi":
            cursor.execute("""
                SELECT p.ad, COUNT(r.id) as risk_sayisi,
                       SUM(CASE WHEN r.etki_seviyesi = 'Yüksek' THEN 1 ELSE 0 END) as yuksek_risk
                FROM projeler p
                LEFT JOIN riskler r ON p.id = r.proje_id
                GROUP BY p.id
            """)
            sonuclar = cursor.fetchall()
            
            rapor = "RİSK ANALİZİ RAPORU\n"
            rapor += "=" * 30 + "\n\n"
            for proje, toplam, yuksek in sonuclar:
                rapor += f"{proje}\n"
                rapor += f"  Toplam Risk: {toplam}\n"
                rapor += f"  Yüksek Riskli: {yuksek}\n\n"
                
        elif rapor_tipi == "Bütçe Durumu":
            cursor.execute("""
                SELECT ad, butce, ilerleme
                FROM projeler
                ORDER BY butce DESC
            """)
            sonuclar = cursor.fetchall()
            
            rapor = "BÜTÇE DURUMU RAPORU\n"
            rapor += "=" * 30 + "\n\n"
            for proje, butce, ilerleme in sonuclar:
                rapor += f"{proje}\n"
                rapor += f"  Bütçe: {butce:,.2f} TL\n"
                rapor += f"  İlerleme: %{ilerleme}\n\n"
                
        else:  # Takım Performansı
            cursor.execute("""
                SELECT k.ad_soyad, k.rol,
                       COUNT(DISTINCT g.id) as toplam_gorev,
                       SUM(CASE WHEN g.durum = 'Tamamlandı' THEN 1 ELSE 0 END) as tamamlanan
                FROM kullanicilar k
                LEFT JOIN gorevler g ON k.id = g.sorumlu_id
                GROUP BY k.id
            """)
            sonuclar = cursor.fetchall()
            
            rapor = "TAKIM PERFORMANSI RAPORU\n"
            rapor += "=" * 30 + "\n\n"
            for kullanici, rol, toplam, tamamlanan in sonuclar:
                rapor += f"{kullanici} ({rol})\n"
                rapor += f"  Toplam Görev: {toplam}\n"
                rapor += f"  Tamamlanan: {tamamlanan}\n"
                rapor += f"  Başarı Oranı: {(tamamlanan/toplam*100 if toplam > 0 else 0):.1f}%\n\n"
        
        self.te_rapor.setText(rapor)

    def yeni_risk_ekle(self):
        row = self.risk_tablosu.rowCount()
        self.risk_tablosu.insertRow(row)
        self.risk_tablosu.setItem(row, 0, QTableWidgetItem("Yeni Risk"))
        self.risk_tablosu.setItem(row, 1, QTableWidgetItem("Orta"))
        self.risk_tablosu.setItem(row, 2, QTableWidgetItem("Orta"))
        self.risk_tablosu.setItem(row, 3, QTableWidgetItem("Önlem planı"))
        self.risk_tablosu.setItem(row, 4, QTableWidgetItem("Aktif"))

    def kullanici_ekle(self):
        ad_soyad = self.le_kullanici_adi.text()
        eposta = self.le_eposta.text()
        rol = self.cb_rol.currentText()
        departman = self.le_departman.text()
        telefon = self.le_telefon.text()
        
        if ad_soyad and eposta:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO kullanicilar (ad_soyad, eposta, rol, departman, telefon) VALUES (?, ?, ?, ?, ?)",
                (ad_soyad, eposta, rol, departman, telefon))
            self.connection.commit()
            
            self.le_kullanici_adi.clear()
            self.le_eposta.clear()
            self.le_departman.clear()
            self.le_telefon.clear()
            QMessageBox.information(self, "Başarılı", "Kullanıcı eklendi.")
        else:
            QMessageBox.warning(self, "Hata", "Lütfen en azından ad soyad ve e-posta alanlarını doldurun.")

    def grafik_olustur(self):
        current_row = self.proje_listesi.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Hata", "Lütfen önce bir proje seçin.")
            return

        proje_adi = self.proje_listesi.item(current_row).text()
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM projeler WHERE ad = ?", (proje_adi,))
        proje_id = cursor.fetchone()[0]

        # Proje ve görevleri yükle
        proje = Proje(proje_adi)
        cursor.execute("""
            SELECT g.baslik, k.ad_soyad, g.durum, g.baslangic_tarihi, g.bitis_tarihi
            FROM gorevler g
            LEFT JOIN kullanicilar k ON g.sorumlu_id = k.id
            WHERE g.proje_id = ?
        """, (proje_id,))
        gorevler = cursor.fetchall()

        for baslik, sorumlu, durum, baslangic_str, bitis_str in gorevler:
            baslangic = datetime.datetime.strptime(baslangic_str, "%Y-%m-%d").date()
            bitis = datetime.datetime.strptime(bitis_str, "%Y-%m-%d").date()
            gorev = Gorev(baslik, sorumlu or "Atanmamış", durum, baslangic, bitis)
            proje.gorev_ekle(gorev)

        grafik_tipi = self.cb_grafik_tipi.currentText()
        if grafik_tipi == "Gantt Şeması":
            self.gantt_semasi_olustur(proje)
        else:
            self.gorev_durum_pastasi_olustur(proje)

    def gantt_semasi_olustur(self, proje):
        fig, ax = plt.subplots(figsize=(14, 7), dpi=400)
        bugun = datetime.date.today()
        bugun_num = mdates.date2num(bugun)

        gorev_adlari = [gorev.adi for gorev in proje.gorevler]
        ax.set_yticks(range(len(gorev_adlari)))
        ax.set_yticklabels(gorev_adlari)

        gorev_renkleri = {
            "Tamamlandı": "green",
            "Devam Ediyor": "orange",
            "Atandı": "lightskyblue"
        }

        for i, gorev in enumerate(proje.gorevler):
            baslangic_num = mdates.date2num(gorev.baslangic)
            bitis_num = mdates.date2num(gorev.bitis)
            sure = max(0, bitis_num - baslangic_num)

            progress_percentage = 0
            toplam_task_sure_num = bitis_num - baslangic_num

            if gorev.durum == "Tamamlandı":
                progress_percentage = 100
            elif gorev.durum == "Devam Ediyor":
                if toplam_task_sure_num > 0 and bugun_num >= baslangic_num and bugun_num <= bitis_num:
                    gecen_sure_num = bugun_num - baslangic_num
                    progress_percentage = min((gecen_sure_num / toplam_task_sure_num) * 100, 99)
                elif bugun_num > bitis_num and gorev.durum != "Tamamlandı":
                    progress_percentage = 99
                elif toplam_task_sure_num <= 0 and bugun_num >= baslangic_num:
                    progress_percentage = 50
                else:
                    progress_percentage = 0
            elif gorev.durum == "Atandı":
                progress_percentage = 0

            progress_percentage = max(0, progress_percentage)

            ax.barh(gorev.adi, sure, left=baslangic_num, height=0.6,
                    color='lightgrey', edgecolor='grey', zorder=1, label='nolegend')

            if progress_percentage > 0:
                progress_bar_width = sure * (progress_percentage / 100.0)
                fill_color = gorev_renkleri.get(gorev.durum, "blue")
                edge_color_progress = 'black'
                if progress_percentage >= 100:
                    edge_color_progress = fill_color

                ax.barh(gorev.adi, progress_bar_width, left=baslangic_num, height=0.6,
                        color=fill_color, edgecolor=edge_color_progress, zorder=2, label='nolegend')

            text_x_position = baslangic_num + sure / 2
            if sure == 0:
                text_x_position = baslangic_num + 0.05

            ax.text(text_x_position, i,
                    f"{gorev.sorumlu} ({progress_percentage:.0f}%)",
                    ha='center', va='center', color='black', fontsize=8, zorder=3,
                    bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.2', edgecolor='none'))

        handles = []
        labels = []
        used_statuses = sorted(list(set(g.durum for g in proje.gorevler if g.durum in gorev_renkleri)))
        for status in used_statuses:
            handles.append(plt.Rectangle((0, 0), 1, 1, color=gorev_renkleri[status]))
            labels.append(status)

        if proje.gorevler:
            today_line = ax.axvline(bugun_num, color='red', linestyle='--', linewidth=1.5, 
                                  label=f'Bugün ({bugun.strftime("%Y-%m-%d")})', zorder=4)
            ax.legend(loc='upper right')
        else:
            ax.legend(handles=handles, labels=labels, loc='upper right')

        ax.set_xlabel("Tarih")
        ax.set_ylabel("Görevler")
        ax.set_title(f"Proje: {proje.proje_adi} - Gantt Şeması (İlerleme Yüzdeleriyle)")

        ax.xaxis_date()
        date_format = mdates.DateFormatter('%Y-%m-%d')
        ax.xaxis.set_major_formatter(date_format)
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
        ax.xaxis.set_minor_locator(mdates.DayLocator())

        fig.autofmt_xdate(rotation=45)
        plt.grid(True, which='major', axis='x', linestyle='--', linewidth='0.5', color='darkgray')
        plt.grid(True, which='minor', axis='x', linestyle=':', linewidth='0.3', color='lightgray')
        plt.tight_layout()
        plt.show()

    def gorev_durum_pastasi_olustur(self, proje):
        istatistikler = proje.gorev_durum_istatistikleri()
        etiketler = list(istatistikler.keys())
        boyutlar = list(istatistikler.values())
        renkler_map = {
            "Tamamlandı": "green",
            "Devam Ediyor": "orange",
            "Atandı": "lightskyblue"
        }
        renkler_liste = [renkler_map.get(etiket, "blue") for etiket in etiketler]

        fig1, ax1 = plt.subplots(figsize=(8, 8))
        ax1.pie(boyutlar, labels=etiketler, autopct='%1.1f%%', startangle=90, colors=renkler_liste,
                wedgeprops={'edgecolor': 'black'})
        ax1.axis('equal')
        plt.title(f"Proje: {proje.proje_adi} - Görev Durumları Dağılımı")
        plt.show()

    def closeEvent(self, event):
        self.connection.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProjeTakipApp()
    window.show()
    sys.exit(app.exec())