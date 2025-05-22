from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, 
    QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class LoginUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(20)

        # Başlık
        title = QLabel("Destek Sistemi Giriş")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #4CAF50;")
        self.layout.addWidget(title)

        # Kullanıcı adı girişi
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Kullanıcı Adı")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        self.layout.addWidget(self.username_input)

        # Şifre girişi
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Şifre")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        self.layout.addWidget(self.password_input)

        # Giriş butonu
        self.login_button = QPushButton("Giriş Yap")
        self.login_button.setStyleSheet("""
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
        self.layout.addWidget(self.login_button)

        # Kayıt butonları
        self.register_staff_button = QPushButton("Personel Kayıt")
        self.register_staff_button.setStyleSheet("""
            QPushButton {
                background-color: #FFC107;
                color: black;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e6ac00;
            }
        """)
        self.layout.addWidget(self.register_staff_button)

        self.register_customer_button = QPushButton("Müşteri Kayıt")
        self.register_customer_button.setStyleSheet("""
            QPushButton {
                background-color: #FFC107;
                color: black;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e6ac00;
            }
        """)
        self.layout.addWidget(self.register_customer_button) 