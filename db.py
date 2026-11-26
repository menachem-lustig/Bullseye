from schema import get_connection


def insert_game(secret_code):
    connector = get_connection()
    try:
        cursor = connector.cursor()
        colors = ' '.join(secret_code)
        cursor.execute("INSERT INTO games (secret_code, attempts_used) VALUES (%s, %s)",
                       (colors, 0))
        connector.commit()
        new_id = cursor.lastrowid
    finally:
        connector.close()
    return new_id


def get_game(game_id):
    connector = get_connection()
    try:
        cursor = connector.cursor(dictionary=True)
        cursor.execute("SELECT * FROM games WHERE id=%s", (game_id,))
        return cursor.fetchone()
    finally:
        connector.close()


def update_game(game_id, attempts_used, status):
    connector = get_connection()
    try:
        cursor = connector.cursor()
        cursor.execute("UPDATE games SET attempts_used=%s, status=%s WHERE id=%s",
                       (attempts_used, status, game_id))
        connector.commit()
    finally:
        connector.close()