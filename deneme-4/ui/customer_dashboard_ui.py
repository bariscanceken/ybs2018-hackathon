from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class CustomerDashboardUI(QWidget):
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
        self.welcome_label = QLabel("Hoş Geldiniz, [Kullanıcı Adı]")
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

        # Yeni talep butonu
        self.new_request_button = QPushButton("Yeni Talep Oluştur")
        self.new_request_button.setStyleSheet("""
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
        self.layout.addWidget(self.new_request_button)

        # Talepler başlığı
        requests_title = QLabel("Taleplerim")
        requests_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        requests_title.setStyleSheet("color: #333333;")
        self.layout.addWidget(requests_title)

        # Talepler tablosu
        self.requests_table = QTableWidget()
        self.requests_table.setColumnCount(6)
        self.requests_table.setHorizontalHeaderLabels([
            "ID", "Başlık", "Kategori", "Öncelik", "Durum", "Tarih"
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