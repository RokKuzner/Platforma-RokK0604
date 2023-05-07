import sqlite3
import random
from datetime import date, datetime
import json
import string

conn = sqlite3.connect("database.db", check_same_thread=False)
c = conn.cursor()


def symbol_to_player(symbol):
    return 1 if symbol == 'X' else -1 if symbol == 'O' else 0


def grid_str_to_obj(s):
    grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    if len(s) != 9 or len([x for x in s if x not in ['X', 'O', '#']]) != 0:
        return None

    for i in range(3):
        for j in range(3):
            grid[i][j] = symbol_to_player(s[i * 3 + j])

    return grid


def get_device_info(device_id):
    c.execute("""
    SELECT * FROM devices WHERE device_id=?
    """, (device_id, ))

    row = c.fetchone()
    return None if not row else {"user": row[0], "device_id": row[1], "game_id": row[2]}

def is_user_in_game(user, game_id):
    c.execute(
        """
    SELECT * FROM tictactoe
    WHERE game_id=? AND (player_x=? OR player_o=?)
    """, (game_id, user, user))

    r = c.fetchone()
    print(f'is_user_in_game {user}, {game_id}', r)

    return r

def assign_game_to_device(device_id, game_id):
    c.execute("""
    UPDATE devices
    SET game_id=?
    WHERE device_id=?
    """, (game_id, device_id))
    conn.commit()

# Lists all not ended games with user
def list_available_games(user_id):
    c.execute("""
        SELECT * FROM tictactoe
        WHERE (player_x=? OR player_o=?) AND ended=false;
    """, (user_id, user_id))
    return c.fetchall()