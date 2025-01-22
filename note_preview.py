from PyQt6.QtWidgets import QDialog, QVBoxLayout, QScrollArea, QSizePolicy, QLabel, QPushButton, QLineEdit, QTextEdit, QWidget, QHBoxLayout, QFrame
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSignal, QPoint

class NotePreview(QDialog):
    delete_note = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.notes_widget = parent  # Сохраняем ссылку на объект NotesWidget
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowTitle("Предпросмотр заметки")
        self.setGeometry(200, 200, 600, 400)
        self._drag_position = None
        self.initUI()

    def initUI(self):
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

        self.layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setReadOnly(True)
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
        self.layout.addWidget(self.title_input)

        self.content_label = QLabel("Текст заметки")
        self.content_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_label.setFont(QFont("Comfortaa", 12))
        self.content_label.setWordWrap(True)
        self.content_label.setTextFormat(Qt.TextFormat.RichText)
        self.content_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.TextSelectableByKeyboard)
        self.layout.addWidget(self.content_label)

        self.content_input = QTextEdit()
        self.content_input.setReadOnly(True)
        self.content_input.setStyleSheet("""
            QTextEdit {
                background-color: #495057;
                color: #FFFFFF;
                border: none;
                margin: 3px 0px;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
        """)
        self.layout.addWidget(self.content_input)

        self.category_label = QLabel("Категория")
        self.category_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.category_label.setFont(QFont("Comfortaa", 10, QFont.Weight.Bold))
        self.layout.addWidget(self.category_label)

        self.category_input = QLineEdit()
        self.category_input.setReadOnly(True)
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
        self.layout.addWidget(self.category_input)

        self.edit_button = QPushButton("Редактировать")
        self.edit_button.setStyleSheet("""
                    QPushButton {
                        background-color: #FFC107;
                        color: #FFFFFF;
                        border: none;
                        border-radius: 5px;
                        padding: 5px;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background-color: #e0a800;
                    }
                """)
        self.edit_button.clicked.connect(self.enable_editing)
        self.layout.addWidget(self.edit_button)

        self.save_button = QPushButton("Сохранить")
        self.save_button.setStyleSheet("""
                    QPushButton {
                        background-color: #28A745;
                        color: #FFFFFF;
                        border: none;
                        border-radius: 5px;
                        padding: 5px;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background-color: #218838;
                    }
                """)
        self.save_button.clicked.connect(self.save_note)
        self.save_button.hide()
        self.layout.addWidget(self.save_button)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.setStyleSheet("""
                    QPushButton {
                        background-color: #DC3545;
                        color: #FFFFFF;
                        border: none;
                        margin: 3px 0px;
                        border-radius: 5px;
                        padding: 5px;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background-color: #c82333;
                    }
                """)
        self.delete_button.clicked.connect(self.delete_current_note)
        self.layout.addWidget(self.delete_button)

        main_layout.addLayout(self.layout)
        self.setLayout(main_layout)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        self.apply_theme(True)  # Устанавливаем тёмную тему по умолчанию

    def apply_theme(self, is_dark_theme):
        if is_dark_theme:
            self.setStyleSheet("""
                background-color: rgba(18, 18, 18, 0.9);
                color: #FFFFFF;
                font-family: 'Segoe UI', Arial, sans-serif;
                border-radius: 15px;
            """)
            self.title_label.setStyleSheet("color: #FFFFFF;")
            self.content_label.setStyleSheet("color: #FFFFFF;")
            self.category_label.setStyleSheet("color: #FFFFFF;")
            self.findChild(QWidget, "topPanel").setStyleSheet("background-color: #121212; border-top-left-radius: 15px; border-top-right-radius: 15px;")
        else:
            self.setStyleSheet("""
                background-color: rgba(255, 255, 255, 0.9);
                color: #000000;
                font-family: 'Segoe UI', Arial, sans-serif;
                border-radius: 15px;
            """)
            self.title_label.setStyleSheet("color: #000000;")
            self.content_label.setStyleSheet("color: #000000;")
            self.category_label.setStyleSheet("color: #000000;")
            self.findChild(QWidget, "topPanel").setStyleSheet("background-color: #FFFFFF; border-top-left-radius: 15px; border-top-right-radius: 15px;")

    def update_note_preview(self, title, content, category):
        self.title_input.setText(title)
        self.content_input.setPlainText(content)
        self.category_input.setText(str(category))

    def delete_current_note(self):
        title = self.title_input.text()
        self.delete_note.emit(title)
        self.close()

    def enable_editing(self):
        self.title_input.setReadOnly(False)
        self.content_input.setReadOnly(False)
        self.category_input.setReadOnly(False)
        self.edit_button.hide()
        self.save_button.show()

    def save_note(self):
        title = self.title_input.text()
        content = self.content_input.toPlainText()
        category = self.category_input.text()
        tags = []  # Здесь можно добавить теги, если они есть

        self.notes_widget.update_note(self.notes_widget.current_note_id, title, content, category, tags)

        self.title_input.setReadOnly(True)
        self.content_input.setReadOnly(True)
        self.category_input.setReadOnly(True)
        self.save_button.hide()
        self.edit_button.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()
