import logging
import hashlib
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import pyqtSignal
from database import get_user_by_username, add_user
from encryption import encrypt_data, decrypt_data

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class LoginWidget(QWidget):
    login_successful = pyqtSignal(int)

    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        self.apply_theme(True)

    def initUI(self):
        layout = QVBoxLayout()
        self.username_input = QLineEdit(placeholderText="Имя пользователя")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(placeholderText="Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Войти")
        self.login_button.setStyleSheet("""
                    QPushButton {
                        background-color: #007BFF;
                        color: #FFFFFF;
                        border: none;
                        border-radius: 5px;
                        padding: 5px;
                    }
                    QPushButton:hover {
                        background-color: #0056b3;
                    }
                """)
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton("Регистрация")
        self.register_button.setStyleSheet("""
                    QPushButton {
                        background-color: #28A745;
                        color: #FFFFFF;
                        border: none;
                        border-radius: 5px;
                        padding: 5px;
                    }
                    QPushButton:hover {
                        background-color: #218838;
                    }
                """)
        self.register_button.clicked.connect(self.go_to_register)
        layout.addWidget(self.register_button)

        self.theme_button = QPushButton("Переключить тему")
        self.theme_button.setStyleSheet("""
                    QPushButton {
                        background-color: #6C757D;
                        color: #FFFFFF;
                        border: none;
                        border-radius: 5px;
                        padding: 5px;
                    }
                    QPushButton:hover {
                        background-color: #5a6268;
                    }
                """)
        self.theme_button.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_button)

        self.setLayout(layout)

    def toggle_theme(self):
        self.parentWidget().parentWidget().toggle_theme()

    def apply_theme(self, is_dark_theme):
        if is_dark_theme:
            self.setStyleSheet("background-color: #121212; color: #FFFFFF;")
            self.username_input.setStyleSheet("background-color: #495057; color: #FFFFFF; border: none; border-radius: 5px; padding: 5px;")
            self.password_input.setStyleSheet("background-color: #495057; color: #FFFFFF; border: none; border-radius: 5px; padding: 5px;")
        else:
            self.setStyleSheet("background-color: #FFFFFF; color: #000000;")
            self.username_input.setStyleSheet("background-color: #E9ECEF; color: #000000; border: none; border-radius: 5px; padding: 5px;")
            self.password_input.setStyleSheet("background-color: #E9ECEF; color: #000000; border: none; border-radius: 5px; padding: 5px;")

    def check_user(self, username, password):
        try:
            result = get_user_by_username(username)
            if result and decrypt_data(result[0]['password']) == hash_password(password):
                return result[0]['id']
        except Exception as e:
            logging.error(f"Error checking user: {e}")
        return None

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Имя пользователя и пароль не могут быть пустыми.")
            return

        user_id = self.check_user(username, password)
        if user_id:
            self.login_successful.emit(user_id)
        else:
            QMessageBox.warning(self, "Ошибка", "Неверное имя пользователя или пароль.")

    def go_to_register(self):
        self.parentWidget().parentWidget().stacked_widget.setCurrentWidget(
            self.parentWidget().parentWidget().register_widget)

class RegisterWidget(QWidget):
    registration_successful = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        self.apply_theme(True)

    def initUI(self):
        layout = QVBoxLayout()

        self.username_input = QLineEdit(placeholderText="Имя пользователя")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(placeholderText="Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        self.confirm_password_input = QLineEdit(placeholderText="Подтвердите пароль")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.confirm_password_input)

        self.register_button = QPushButton("Зарегистрироваться")
        self.register_button.setStyleSheet("""
                    QPushButton {
                        background-color: #28A745;
                        color: #FFFFFF;
                        border: none;
                        border-radius: 5px;
                        padding: 5px;
                    }
                    QPushButton:hover {
                        background-color: #218838;
                    }
                """)
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.back_button = QPushButton("Назад к входу")
        self.back_button.setStyleSheet("""
                    QPushButton {
                        background-color: #6C757D;
                        color: #FFFFFF;
                        border: none;
                        border-radius: 5px;
                        padding: 5px;
                    }
                    QPushButton:hover {
                        background-color: #5a6268;
                    }
                """)
        self.back_button.clicked.connect(self.go_to_login)
        layout.addWidget(self.back_button)

        self.theme_button = QPushButton("Переключить тему")
        self.theme_button.setStyleSheet("""
                    QPushButton {
                        background-color: #6C757D;
                        color: #FFFFFF;
                        border: none;
                        border-radius: 5px;
                        padding: 5px;
                    }
                    QPushButton:hover {
                        background-color: #5a6268;
                    }
                """)
        self.theme_button.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_button)

        self.setLayout(layout)

    def toggle_theme(self):
        self.parentWidget().parentWidget().toggle_theme()

    def apply_theme(self, is_dark_theme):
        if is_dark_theme:
            self.setStyleSheet("background-color: #121212; color: #FFFFFF;")
            self.username_input.setStyleSheet("background-color: #495057; color: #FFFFFF; border: none; border-radius: 5px; padding: 5px;")
            self.password_input.setStyleSheet("background-color: #495057; color: #FFFFFF; border: none; border-radius: 5px; padding: 5px;")
            self.confirm_password_input.setStyleSheet("background-color: #495057; color: #FFFFFF; border: none; border-radius: 5px; padding: 5px;")
        else:
            self.setStyleSheet("background-color: #FFFFFF; color: #000000;")
            self.username_input.setStyleSheet("background-color: #E9ECEF; color: #000000; border: none; border-radius: 5px; padding: 5px;")
            self.password_input.setStyleSheet("background-color: #E9ECEF; color: #000000; border: none; border-radius: 5px; padding: 5px;")
            self.confirm_password_input.setStyleSheet("background-color: #E9ECEF; color: #000000; border: none; border-radius: 5px; padding: 5px;")

    def add_user(self, username, password):
        try:
            add_user(username, encrypt_data(hash_password(password)))
        except Exception as e:
            logging.error(f"Error adding user: {e}")
            raise

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "Ошибка", "Все поля обязательны для заполнения.")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают.")
            return

        try:
            self.add_user(username, password)
            self.registration_successful.emit()
        except pymysql.IntegrityError:
            QMessageBox.warning(self, "Ошибка", "Имя пользователя уже существует.")

    def go_to_login(self):
        self.parentWidget().parentWidget().stacked_widget.setCurrentWidget(self.parentWidget().parentWidget().login_widget)
