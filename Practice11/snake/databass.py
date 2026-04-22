import sqlite3

def init_db():
    conn = sqlite3.connect("Practice11\\snake\\highscores_snake.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS highscores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT,
            coins INTEGER,
            time_survived REAL
        )
    """)
    conn.commit()
    conn.close()

# Запускаем один раз при старте игры
init_db()


def get_top_scores():
    conn = sqlite3.connect("Practice11\\snake\\highscores_snake.db")
    cursor = conn.cursor()
    # top 5 score 
    cursor.execute("SELECT nickname, score FROM highscores ORDER BY score DESC LIMIT ?", (5,))
    data = cursor.fetchall()
    conn.close()
    return data

def save_score(name, coins, play_time):
    conn = sqlite3.connect("Practice11\\snake\\highscores_snake.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO highscores (nickname, score, time_survived) VALUES (?, ?, ROUND(?, 2))", 
                   (name, coins, play_time))
    conn.commit()
    conn.close()

