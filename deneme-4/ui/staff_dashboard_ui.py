from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QLineEdit, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class StaffDashboardUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        # Üst bar
        top_bar = QHBoxLayout()
        
        # Hoş geldiniz mesajı
        self.welcome_label = QLabel("Hoş Geldiniz, [Personel Adı]")
        self.welcome_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.welcome_label.setStyleSheet("color: #333333;")
        top_bar.addWidget(self.welcome_label)
        
        # Sağ tarafa çıkış butonu
        top_bar.addStretch()
        self.logout_button = QPushButton("Çıkış Yap")
        self.logout_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        top_bar.addWidget(self.logout_button)
        
        self.layout.addLayout(top_bar)

        # Arama ve filtreleme
        search_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Talep ID, Başlık veya Açıklama Ara...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        search_layout.addWidget(self.search_input)
        
        self.search_button = QPushButton("Ara")
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        search_layout.addWidget(self.search_button)
        
        self.layout.addLayout(search_layout)

        # Talepler başlığı
        requests_title = QLabel("Tüm Talepler")
        requests_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        requests_title.setStyleSheet("color: #333333;")
        self.layout.addWidget(requests_title)

        # Talepler tablosu
        self.requests_table = QTableWidget()
        self.requests_table.setColumnCount(10)
        self.requests_table.setHorizontalHeaderLabels([
            "ID", "Talep Sahibi", "Kategori", "Başlık", "Açıklama",
            "Öncelik", "Durum", "Oluşturma Tarihi", "Çözüm Tarihi", "Çözen Personel"
        ])
        self.requests_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.requests_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.requests_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 5px;
                border: 1px solid #4CAF50;
            }
        """)
        self.layout.addWidget(self.requests_table)

        # Talep yönetim butonları
        management_layout = QHBoxLayout()
        
        self.selected_request_label = QLabel("Seçili Talep ID: Yok")
        self.selected_request_label.setFont(QFont("Segoe UI", 12))
        management_layout.addWidget(self.selected_request_label)
        
        management_layout.addStretch()
        
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Beklemede", "Devam Ediyor", "Tamamlandı", "İptal Edildi"])
        self.status_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        management_layout.addWidget(self.status_combo)
        
        self.update_button = QPushButton("Durumu Güncelle")
        self.update_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        management_layout.addWidget(self.update_button)
        
        self.delete_button = QPushButton("Talebi Sil")
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        management_layout.addWidget(self.delete_button)
        
        self.layout.addLayout(management_layout) 