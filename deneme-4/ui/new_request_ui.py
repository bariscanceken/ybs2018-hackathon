from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, 
    QPushButton, QComboBox, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class NewRequestUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        # Başlık
        title = QLabel("Yeni Destek Talebi Oluştur")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #4CAF50;")
        self.layout.addWidget(title)

        # Kategori
        category_label = QLabel("Kategori:")
        category_label.setFont(QFont("Segoe UI", 12))
        self.layout.addWidget(category_label)
        
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Yazılım", "Donanım", "Ağ", "Diğer"])
        self.category_combo.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        self.layout.addWidget(self.category_combo)

        # Başlık
        title_label = QLabel("Başlık:")
        title_label.setFont(QFont("Segoe UI", 12))
        self.layout.addWidget(title_label)
        
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Talebinizin kısa başlığı")
        self.title_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        self.layout.addWidget(self.title_input)

        # Açıklama
        description_label = QLabel("Açıklama:")
        description_label.setFont(QFont("Segoe UI", 12))
        self.layout.addWidget(description_label)
        
        self.description_text = QTextEdit()
        self.description_text.setPlaceholderText("Talebinizin detaylı açıklaması...")
        self.description_text.setStyleSheet("""
            QTextEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        self.layout.addWidget(self.description_text)

        # Öncelik
        priority_label = QLabel("Öncelik:")
        priority_label.setFont(QFont("Segoe UI", 12))
        self.layout.addWidget(priority_label)
        
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Düşük", "Normal", "Yüksek"])
        self.priority_combo.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        self.layout.addWidget(self.priority_combo)

        # Talep oluştur butonu
        self.create_button = QPushButton("Talebi Oluştur")
        self.create_button.setStyleSheet("""
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
        self.layout.addWidget(self.create_button)

        # Geri dön butonu
        self.back_button = QPushButton("Geri Dön")
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        self.layout.addWidget(self.back_button) 