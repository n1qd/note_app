from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QComboBox, QScrollArea, QLabel, QMessageBox, QFrame
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from database import get_notes_by_user_id, get_categories_by_user_id, get_note_by_title_and_user_id, add_note, update_note, delete_note_by_title_and_user_id, get_or_create_tag, add_note_tag, get_tags_by_user_id, filter_notes_by_tag, filter_notes_by_categories, get_or_create_category
from encryption import encrypt_data, decrypt_data
from note_dialog import NoteDialog
from note_preview import NotePreview

class NotesWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.user_id = None
        self.current_note_id = None
        self.notes_cache = {}
        self.categories_cache = {}
        self.tags_cache = {}  # Кэш для тегов
        self.initUI()
        self.apply_theme(True)  # Устанавливаем тёмную тему по умолчанию

    def initUI(self):
        main_layout = QVBoxLayout()

        # Верхняя часть с тегами
        tags_layout = QHBoxLayout()
        tags_label = QLabel("Теги")
        tags_label.setFont(QFont("Comfortaa", 14, QFont.Weight.Bold))
        tags_layout.addWidget(tags_label)

        self.tag_buttons_area = QScrollArea()
        self.tag_buttons_area.setWidgetResizable(True)
        self.tag_buttons_widget = QWidget()
        self.tag_buttons_layout = QHBoxLayout()
        self.tag_buttons_widget.setLayout(self.tag_buttons_layout)
        self.tag_buttons_area.setWidget(self.tag_buttons_widget)
        self.tag_buttons_area.setMaximumHeight(62)
        tags_layout.addWidget(self.tag_buttons_area)

        self.clear_tags_button = QPushButton("Сбросить выбор тегов")
        self.clear_tags_button.setStyleSheet("""
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
        self.clear_tags_button.clicked.connect(self.clear_tags)
        tags_layout.addWidget(self.clear_tags_button)

        main_layout.addLayout(tags_layout)

        # Основная область со списком заметок
        notes_layout = QVBoxLayout()
        notes_label = QLabel("Список заметок")
        notes_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        notes_label.setFont(QFont("Comfortaa", 14, QFont.Weight.Bold))
        notes_layout.addWidget(notes_label)

        self.note_list = QListWidget()
        self.note_list.itemClicked.connect(self.load_note)
        notes_layout.addWidget(self.note_list)

        main_layout.addLayout(notes_layout)

        # Поле поиска и выбора категории
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit(placeholderText="Поиск")
        self.search_input.textChanged.connect(self.search_notes)
        search_layout.addWidget(self.search_input)

        self.category_combo = QComboBox()
        self.category_combo.currentTextChanged.connect(self.filter_notes)
        search_layout.addWidget(self.category_combo)

        main_layout.addLayout(search_layout)

        # Кнопки управления
        buttons_layout = QHBoxLayout()
        self.new_note_button = QPushButton("Новая заметка")
        self.new_note_button.setStyleSheet("""
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
        self.new_note_button.clicked.connect(self.open_new_note_dialog)
        buttons_layout.addWidget(self.new_note_button)

        self.logout_button = QPushButton("Выйти")
        self.logout_button.setStyleSheet("""
                    QPushButton {
                        background-color: #DC3545;
                        color: #FFFFFF;
                        border: none;
                        border-radius: 5px;
                        padding: 5px;
                    }
                    QPushButton:hover {
                        background-color: #c82333;
                    }
                """)
        self.logout_button.clicked.connect(self.logout)
        buttons_layout.addWidget(self.logout_button)

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
        buttons_layout.addWidget(self.theme_button)

        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

        self.note_preview = NotePreview(self)
        self.note_preview.delete_note.connect(self.delete_note)

    def toggle_theme(self):
        self.parent().parent().toggle_theme()

    def apply_theme(self, is_dark_theme):
        if is_dark_theme:
            self.setStyleSheet("background-color: rgba(18, 18, 18, 0.9); color: #FFFFFF;")
            self.note_list.setStyleSheet("background-color: #343A40; color: #FFFFFF;")
            self.search_input.setStyleSheet("background-color: #495057; color: #FFFFFF; border: none; border-radius: 5px; padding: 5px;")
            self.category_combo.setStyleSheet("background-color: #495057; color: #FFFFFF; border: none; border-radius: 5px; padding: 5px;")
            self.tag_buttons_area.setStyleSheet("background-color: #343A40; color: #FFFFFF;")
        else:
            self.setStyleSheet("background-color: rgba(255, 255, 255, 0.9); color: #000000;")
            self.note_list.setStyleSheet("background-color: #E9ECEF; color: #000000;")
            self.search_input.setStyleSheet("background-color: #E9ECEF; color: #000000; border: none; border-radius: 5px; padding: 5px;")
            self.category_combo.setStyleSheet("background-color: #E9ECEF; color: #000000; border: none; border-radius: 5px; padding: 5px;")
            self.tag_buttons_area.setStyleSheet("background-color: #E9ECEF; color: #000000;")

    def load_notes(self, user_id):
        if user_id in self.notes_cache:
            notes = self.notes_cache[user_id]
        else:
            notes = get_notes_by_user_id(user_id)
            self.notes_cache[user_id] = notes
        self.note_list.clear()
        for note in notes:
            self.note_list.addItem(note['title'])

    def load_categories(self, user_id):
        if user_id in self.categories_cache:
            categories = self.categories_cache[user_id]
        else:
            categories = get_categories_by_user_id(user_id)
            self.categories_cache[user_id] = categories
        self.category_combo.clear()
        self.category_combo.addItem("Все категории")
        for category in categories:
            self.category_combo.addItem(category['name'])

    def load_tags(self, user_id):
        if user_id in self.tags_cache:
            self.tags_cache[user_id] = get_tags_by_user_id(user_id)
            tags = self.tags_cache[user_id]
        else:
            tags = get_tags_by_user_id(user_id)
            self.tags_cache[user_id] = tags

        # Очистка и добавление кнопок тегов
        for i in reversed(range(self.tag_buttons_layout.count())):
            self.tag_buttons_layout.itemAt(i).widget().setParent(None)

        for tag in tags:
            tag_button = QPushButton(tag['name'])
            tag_button.setStyleSheet("""
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
            tag_button.clicked.connect(lambda _, t=tag['name']: self.filter_notes_by_tag(t))
            self.tag_buttons_layout.addWidget(tag_button)

    def load_note(self, item):
        title = item.text()
        note = get_note_by_title_and_user_id(title, self.user_id)
        if note:
            note = note[0]
            self.current_note_id = note['id']
            self.note_preview.update_note_preview(title, decrypt_data(note['content']) if 'content' in note else '', str(note['category_name']))
            self.note_preview.show()

    def open_new_note_dialog(self):
        dialog = NoteDialog(self, is_new=True)
        dialog.exec()

    def open_edit_note_dialog(self):
        if not self.current_note_id:
            QMessageBox.warning(self, "Ошибка", "Нет заметки для редактирования.")
            return

        dialog = NoteDialog(self, is_new=False)
        dialog.exec()

    def save_note(self, title, content, category, tags):
        if not title or not content:
            QMessageBox.warning(self, "Ошибка", "Заголовок и содержание не могут быть пустыми.")
            return

        try:
            category_id = get_or_create_category(category)
            note_id = add_note(self.user_id, title, encrypt_data(content), category_id)

            for tag in tags:
                tag = tag.strip()
                if tag:
                    tag_id = get_or_create_tag(tag)
                    add_note_tag(note_id, tag_id)

            self.load_notes(self.user_id)
            self.load_categories(self.user_id)
            self.load_tags(self.user_id)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить заметку: {e}")

    def update_note(self, note_id, title, content, category, tags):
        if not title or not content:
            QMessageBox.warning(self, "Ошибка", "Заголовок и содержание не могут быть пустыми.")
            return

        category_id = get_or_create_category(category)
        update_note(note_id, title, encrypt_data(content), category_id)
        self.load_notes(self.user_id)
        self.load_categories(self.user_id)

    def delete_note(self, title):
        delete_note_by_title_and_user_id(title, self.user_id)
        self.load_notes(self.user_id)
        self.load_categories(self.user_id)
        self.clear_fields()

    def clear_fields(self):
        self.current_note_id = None

    def search_notes(self, text):
        notes = get_notes_by_user_id(self.user_id)
        self.note_list.clear()
        for note in notes:
            if text.lower() in note['title'].lower() or (text.lower() in decrypt_data(note['content']).lower() if 'content' in note else False):
                self.note_list.addItem(note['title'])

    def filter_notes(self, category):
        if category == "Все категории":
            notes = get_notes_by_user_id(self.user_id)
        else:
            notes = filter_notes_by_categories(self.user_id, category)
        self.note_list.clear()
        for note in notes:
            self.note_list.addItem(note['title'])

    def filter_notes_by_tag(self, tag):
        if tag == "Все теги":
            notes = get_notes_by_user_id(self.user_id)
        else:
            notes = filter_notes_by_tag(self.user_id, tag)
        self.note_list.clear()
        for note in notes:
            self.note_list.addItem(note['title'])

    def logout(self):
        self.user_id = None
        self.clear_fields()
        self.note_list.clear()
        self.category_combo.clear()
        self.parent().parent().restart_app()

    def clear_tags(self):
        self.category_combo.setCurrentIndex(0)
        self.load_notes(self.user_id)
