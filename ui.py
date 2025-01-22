from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QMainWindow, QLabel, QPushButton, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt, QPoint
from auth import LoginWidget, RegisterWidget
from notes_widget import NotesWidget

class NoteApp(QWidget):
    def __init__(self):
        super().__init__()
        self.user_id = None
        self.is_dark_theme = True
        self.initUI()
        self.setFixedSize(320, 320)
        self._drag_position = None

    def initUI(self):
        self.setWindowTitle("Заметки")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Верхняя панель
        top_panel = QWidget()
        top_panel.setObjectName("topPanel")
        top_panel_layout = QHBoxLayout()
        top_panel_layout.setContentsMargins(10, 10, 10, 10)
        self.title_label = QLabel("Заметки")
        self.title_label.setStyleSheet("color: white; font-size: 16px;")
        top_panel_layout.addWidget(self.title_label)

        top_panel_layout.addStretch()

        self.minimize_button = QPushButton("−")
        self.minimize_button.setFixedSize(30, 30)
        self.minimize_button.setStyleSheet("""
            QPushButton {
                background-color: yellow;
                color: black;
                border-radius: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: olive;
            }
        """)
        self.minimize_button.clicked.connect(self.showMinimized)
        top_panel_layout.addWidget(self.minimize_button)

        self.close_button = QPushButton("X")
        self.close_button.setFixedSize(30, 30)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border-radius: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        self.close_button.clicked.connect(self.close)
        top_panel_layout.addWidget(self.close_button)

        top_panel.setLayout(top_panel_layout)
        main_layout.addWidget(top_panel)

        self.stacked_widget = QStackedWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)

        self.login_widget = LoginWidget(self.stacked_widget)
        self.login_widget.login_successful.connect(self.on_login_successful)
        self.stacked_widget.addWidget(self.login_widget)

        self.register_widget = RegisterWidget(self.stacked_widget)
        self.register_widget.registration_successful.connect(self.on_registration_successful)
        self.stacked_widget.addWidget(self.register_widget)

        main_layout.addLayout(layout)
        self.setLayout(main_layout)

        # Автоматическое применение цветовой темы при запуске
        self.apply_theme(self.is_dark_theme)

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme(self.is_dark_theme)

    def apply_theme(self, is_dark_theme):
        if is_dark_theme:
            self.setStyleSheet("""
                background-color: rgba(18, 18, 18, 0.9);
                color: #FFFFFF;
                font-family: 'Comfortaa', sans-serif;
                border-radius: 15px;
            """)
            self.title_label.setStyleSheet("color: #FFFFFF;")
            self.findChild(QWidget, "topPanel").setStyleSheet("background-color: #121212; border-top-left-radius: 15px; border-top-right-radius: 15px;")
        else:
            self.setStyleSheet("""
                background-color: rgba(255, 255, 255, 0.9);
                color: #000000;
                font-family: 'Comfortaa', sans-serif;
                border-radius: 15px;
            """)
            self.title_label.setStyleSheet("color: #000000;")
            self.findChild(QWidget, "topPanel").setStyleSheet("background-color: #FFFFFF; border-top-left-radius: 15px; border-top-right-radius: 15px;")

        self.login_widget.apply_theme(is_dark_theme)
        self.register_widget.apply_theme(is_dark_theme)

    def on_login_successful(self, user_id):
        self.user_id = user_id
        self.hide()  # Hide the login window
        self.main_window = MainWindow(user_id, self.is_dark_theme)
        self.main_window.show()

    def on_registration_successful(self):
        self.stacked_widget.setCurrentWidget(self.login_widget)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()

class MainWindow(QMainWindow):
    def __init__(self, user_id, is_dark_theme):
        super().__init__()
        self.user_id = user_id
        self.is_dark_theme = is_dark_theme
        self.initUI()
        self._drag_position = None

    def initUI(self):
        self.setWindowTitle("Заметки")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Верхняя панель
        top_panel = QWidget()
        top_panel.setObjectName("topPanel")
        top_panel_layout = QHBoxLayout()
        top_panel_layout.setContentsMargins(10, 10, 10, 10)
        self.title_label = QLabel("Заметки")
        self.title_label.setStyleSheet("color: white; font-size: 16px;")
        top_panel_layout.addWidget(self.title_label)

        top_panel_layout.addStretch()

        self.minimize_button = QPushButton("−")
        self.minimize_button.setFixedSize(30, 30)
        self.minimize_button.setStyleSheet("""
            QPushButton {
                background-color: yellow;
                color: black;
                border-radius: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: olive;
            }
        """)
        self.minimize_button.clicked.connect(self.showMinimized)
        top_panel_layout.addWidget(self.minimize_button)

        self.close_button = QPushButton("X")
        self.close_button.setFixedSize(30, 30)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border-radius: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        self.close_button.clicked.connect(self.close)
        top_panel_layout.addWidget(self.close_button)

        top_panel.setLayout(top_panel_layout)
        main_layout.addWidget(top_panel)

        self.notes_widget = NotesWidget(self)
        main_layout.addWidget(self.notes_widget)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.notes_widget.user_id = self.user_id
        self.notes_widget.load_notes(self.user_id)
        self.notes_widget.load_categories(self.user_id)
        self.notes_widget.load_tags(self.user_id)

        self.apply_theme(self.is_dark_theme)

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme(self.is_dark_theme)

    def apply_theme(self, is_dark_theme):
        if is_dark_theme:
            self.setStyleSheet("""
                background-color: rgba(18, 18, 18, 0.9);
                color: #FFFFFF;
                font-family: 'Comfortaa', sans-serif;
                border-radius: 10px;
            """)
            self.title_label.setStyleSheet("color: #FFFFFF;")
            self.findChild(QWidget, "topPanel").setStyleSheet("background-color: #121212; border-top-left-radius: 15px; border-top-right-radius: 15px;")
        else:
            self.setStyleSheet("""
                background-color: rgba(255, 255, 255, 0.9);
                color: #000000;
                font-family: 'Comfortaa', sans-serif;
                border-radius: 10px;
            """)
            self.title_label.setStyleSheet("color: #000000;")
            self.findChild(QWidget, "topPanel").setStyleSheet("background-color: #FFFFFF; border-top-left-radius: 15px; border-top-right-radius: 15px;")

        self.notes_widget.apply_theme(is_dark_theme)
        self.notes_widget.note_preview.apply_theme(is_dark_theme)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()

    def restart_app(self):
        self.close()


