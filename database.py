import sqlite3

def create_database():
    conn = sqlite3.connect('notes.db')
    with conn:
        # Создаем таблицу users
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)

        # Создаем таблицу categories
        conn.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)

        # Создаем таблицу notes
        conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                category_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        """)

        # Создаем таблицу tags
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)

        # Создаем таблицу note_tags
        conn.execute("""
            CREATE TABLE IF NOT EXISTS note_tags (
                note_id INTEGER NOT NULL,
                tag_id INTEGER NOT NULL,
                PRIMARY KEY (note_id, tag_id),
                FOREIGN KEY (note_id) REFERENCES notes (id),
                FOREIGN KEY (tag_id) REFERENCES tags (id)
            )
        """)
    conn.close()

def execute_query(query, params=None, return_id=False):
    conn = sqlite3.connect('notes.db')
    with conn:
        c = conn.cursor()
        if params:
            c.execute(query, params)
        else:
            c.execute(query)
        conn.commit()
        if return_id:
            result = c.lastrowid
        else:
            result = c.fetchall()
    conn.close()
    return result

def get_user_by_username(username):
    query = "SELECT id, password FROM users WHERE username = ?"
    return execute_query(query, (username,))

def add_user(username, password):
    query = "INSERT INTO users (username, password) VALUES (?, ?)"
    execute_query(query, (username, password))

def get_notes_by_user_id(user_id):
    query = "SELECT id, title FROM notes WHERE user_id = ?"
    return execute_query(query, (user_id,))

def get_categories_by_user_id(user_id):
    query = "SELECT DISTINCT c.name FROM notes n JOIN categories c ON n.category_id = c.id WHERE n.user_id = ?"
    return execute_query(query, (user_id,))

def get_note_by_title_and_user_id(title, user_id):
    query = ("""SELECT notes.id, notes.content, categories.name AS category_name
             FROM notes
             JOIN categories ON notes.category_id = categories.id
             WHERE notes.title = ? AND notes.user_id = ?""")
    return execute_query(query, (title, user_id))

def add_note(user_id, title, content, category_id):
    query = "INSERT INTO notes (user_id, title, content, category_id) VALUES (?, ?, ?, ?)"
    return execute_query(query, (user_id, title, content, category_id), return_id=True)

def update_note(note_id, title, content, category_id):
    query = "UPDATE notes SET title = ?, content = ?, category_id = ? WHERE id = ?"
    execute_query(query, (title, content, category_id, note_id))

def delete_note_by_title_and_user_id(title, user_id):
    query = "DELETE FROM notes WHERE title = ? AND user_id = ?"
    execute_query(query, (title, user_id))

def get_or_create_tag(tag_name):
    query = "SELECT id FROM tags WHERE name = ?"
    result = execute_query(query, (tag_name,))
    if result:
        return result[0][0]
    else:
        query = "INSERT INTO tags (name) VALUES (?)"
        return execute_query(query, (tag_name,), return_id=True)

def add_note_tag(note_id, tag_id):
    query = "INSERT INTO note_tags (note_id, tag_id) VALUES (?, ?)"
    execute_query(query, (note_id, tag_id))

def get_tags_by_user_id(user_id):
    query = "SELECT DISTINCT t.name FROM notes n JOIN note_tags nt ON n.id = nt.note_id JOIN tags t ON nt.tag_id = t.id WHERE n.user_id = ?"
    return execute_query(query, (user_id,))

def filter_notes_by_tag(user_id, tag):
    query = """
        SELECT n.id, n.title
        FROM notes n
        JOIN note_tags nt ON n.id = nt.note_id
        JOIN tags t ON nt.tag_id = t.id
        WHERE n.user_id = ? AND t.name = ?
    """
    return execute_query(query, (user_id, tag))

def filter_notes_by_categories(user_id, category):
    query = """
        SELECT n.id, n.title
        FROM notes n
        JOIN categories c ON n.category_id = c.id
        WHERE n.user_id = ? AND c.name = ?
    """
    return execute_query(query, (user_id, category))

def get_or_create_category(category_name):
    query = "SELECT id FROM categories WHERE name = ?"
    result = execute_query(query, (category_name,))
    if result:
        return result[0][0]
    else:
        query = "INSERT INTO categories (name) VALUES (?)"
        return execute_query(query, (category_name,), return_id=True)
