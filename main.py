import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from ui import NoteApp
from database import create_database

def main():
    create_database()  # Создание базы данных при запуске
    app = QApplication(sys.argv)
    ex = NoteApp()
    ex.setWindowFlag(Qt.WindowType.FramelessWindowHint)
    ex.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    ex.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
