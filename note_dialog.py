from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QWidget, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, pyqtSignal, QPoint

class NoteDialog(QDialog):
    def __init__(self, parent, is_new):
        super().__init__(parent)
        self.is_new = is_new
        self.parent = parent
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.initUI()
        self._drag_position = None

    def initUI(self):
        self.setWindowTitle("Новая заметка" if self.is_new else "Редактировать заметку")
        self.setGeometry(200, 200, 600, 400)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Верхняя панель
        top_panel = QWidget()
        top_panel.setObjectName("topPanel")
        top_panel_layout = QHBoxLayout()
        top_panel_layout.setContentsMargins(10, 10, 10, 10)
        self.title_label = QLabel(self.windowTitle())
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

        layout = QVBoxLayout()
        self.title_input = QLineEdit(placeholderText="Заголовок")
        self.title_input.setStyleSheet("""
            QLineEdit {
                background-color: #495057;
                color: #FFFFFF;
                border: none;
                margin: 3px 0px;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.title_input)

        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText("Содержание заметки")
        self.content_input.setStyleSheet("""
            QTextEdit {
                background-color: #495057;
                color: #FFFFFF;
                border: none;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.content_input)

        self.category_input = QLineEdit(placeholderText="Категория")
        self.category_input.setStyleSheet("""
            QLineEdit {
                background-color: #495057;
                color: #FFFFFF;
                border: none;
                margin: 3px 0px;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.category_input)

        self.tag_input = QLineEdit(placeholderText="Теги (через запятую)")
        self.tag_input.setStyleSheet("""
            QLineEdit {
                background-color: #495057;
                color: #FFFFFF;
                border: none;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.tag_input)

        self.save_button = QPushButton("Сохранить")
        self.save_button.setStyleSheet("""
                    QPushButton {
                        background-color: #28A745;
                        color: #FFFFFF;
                        border: none;
                        margin: 3px 0px;
                        border-radius: 5px;
                        padding: 5px;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background-color: #218838;
                    }
                """)
        self.save_button.clicked.connect(self.save_note)
        layout.addWidget(self.save_button)

        main_layout.addLayout(layout)
        self.setLayout(main_layout)

    def save_note(self):
        title = self.title_input.text()
        content = self.content_input.toPlainText()
        category = self.category_input.text()
        tags = self.tag_input.text().split(',')

        if self.is_new:
            self.parent.save_note(title, content, category, tags)
        else:
            self.parent.update_note(self.parent.current_note_id, title, content, category, tags)

        self.close()

    def apply_theme(self, is_dark_theme):
        if is_dark_theme:
            self.setStyleSheet("""
                background-color: rgba(18, 18, 18, 0.9);
                color: #FFFFFF;
                font-family: 'Segoe UI', Arial, sans-serif;
                border-radius: 15px;
            """)
            self.title_label.setStyleSheet("color: #FFFFFF;")
            self.findChild(QWidget, "topPanel").setStyleSheet("background-color: #121212; border-top-left-radius: 15px; border-top-right-radius: 15px;")
        else:
            self.setStyleSheet("""
                background-color: rgba(255, 255, 255, 0.9);
                color: #000000;
                font-family: 'Segoe UI', Arial, sans-serif;
                border-radius: 15px;
            """)
            self.title_label.setStyleSheet("color: #000000;")
            self.findChild(QWidget, "topPanel").setStyleSheet("background-color: #FFFFFF; border-top-left-radius: 15px; border-top-right-radius: 15px;")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()
