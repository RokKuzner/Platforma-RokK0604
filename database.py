import sqlite3
import random
from datetime import date, datetime
import json
import string

conn = sqlite3.connect("database.db", check_same_thread=False)
c = conn.cursor()

def generate_id(table_name, id_field):

    while True:
        id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        c.execute(f'SELECT * FROM {table_name} WHERE {id_field}=?', (id, ))
        if c.fetchone() is None:
            break
        
    return id

# function should return all users from db
def get_users():
    c.execute("SELECT username FROM users;")
    users = c.fetchall()
    return users


def validate_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, password))
    return c.fetchone() is not None


def add_user(username, email, password):
    # function should all user to db
    c.execute("INSERT INTO users VALUES(?, ?, ?)", (username, email, password))
    conn.commit()
    return "user added to db"


def user_exists(username, email):
    # function should check if username or email are already used in database
    c.execute("SELECT * FROM users WHERE username = ? OR email=?",
              (username, email))
    if len(c.fetchall()) == 0:
        return False
    return True


# function should return all rooms in db
def get_rooms():
    c.execute("SELECT * FROM rooms;")
    rooms = c.fetchall()
    return rooms


# function should retrurn all rooms with selected username
def get_rooms_with_username(username):
    c.execute("SELECT * FROM rooms WHERE room_owner = ?;", (username, ))
    return c.fetchall()


def create_room(user, name):
    id = random.randint(1, 10000)
    c.execute("INSERT INTO rooms VALUES (?, ?, ?, ?);",
              (id, name, user, date.today()))
    conn.commit()  # dodati moramo še commit ker zapisujemo v bazo
    return id


def join_room(room, user):
    c.execute("INSERT INTO user_in_room VALUES (?, ?)", (room, user))
    conn.commit()


def get_rooms_with_username2(username):
    c.execute("SELECT * FROM user_in_room WHERE username = ?;", (username, ))
    return c.fetchall()


def get_room_name_from_id(room):
    #name = "ime ki ga dobimo iz baze"
    # select stavek kjer preko ID-ja dobimo ime
    c.execute("SELECT name FROM rooms WHERE id=?;", (room, ))
    return c.fetchone()[0]


def user_not_in_room(room, user):
    # preverimo ali je user že v tej sobi
    c.execute("SELECT * FROM user_in_room WHERE room_id = ? AND username = ?",
              (room, user))
    if len(c.fetchall()) == 0:
        return True
    return False


def room_exists(room):  # podamo ID
    # funkcija vrne True ali False - True če soba ostaja, False če ne
    c.execute("SELECT * FROM rooms WHERE id = ?", (room, ))
    if len(c.fetchall()) == 0:
        return False
    return True


def get_users_in_room(room):  # podamo ID rooma
    # funkcija naj vrne seznam userjev
    c.execute("SELECT username FROM user_in_room WHERE room_id = ?", (room, ))
    return c.fetchall()
    # return ["miha", "test", "mark"]


def get_messages(room):
    #     # funkcija naj vrne vsa sporočila od vseh userjev za to sobo
    # TODO: funkacija na vrne samo sporočila za to sobo - room
    c.execute(
        "SELECT * FROM messages WHERE room_id = ? ORDER BY date DESC LIMIT 5;",
        (room, ))
    messages = []
    raw = c.fetchall()
    for r in raw:
        temp = {}
        temp["username"] = r[0]
        temp["text"] = r[1]
        temp["date"] = r[3]
        messages.append(temp)
    return messages


# TODO: dokončaj funkcijo add_messages
def add_message_to_room(username, message, room):
    date = datetime.now()
    c.execute("INSERT INTO messages VALUES(?, ?, ?, ?)",
              (username, message, room, date))
    conn.commit()


def is_room_owner(user, room):
    c.execute("SELECT * FROM rooms WHERE id=? AND room_owner=?", (room, user))

    return len(c.fetchall()) != 0


def remove_user_from_room(user, room):
    c.execute("DELETE FROM user_in_room WHERE username = ? AND room_id = ?",
              (user, room))
    conn.commit()


def get_tictactoe(game_id):
    c.execute("SELECT * FROM tictactoe WHERE game_id=?", (game_id, ))

    game = c.fetchone()

    if game is None:
        return None
    
    return {
        "game_id": game[0],
        "room_id": game[1],
        "player_x": game[2],
        "player_o": game[3],
        "state": json.loads(game[4])["state"],
        "next_player": game[5],
        "winner": game[6],
        "ended": game[7]
    }

def update_tictactoe_state(game_id, new_state, next_player):
    print('update state', new_state)
    state_str = json.dumps({'state': new_state})
    
    c.execute("""
    UPDATE tictactoe
    SET state=?, next_player=?
    WHERE game_id=?
    """, (state_str, next_player, game_id))

    conn.commit()

def update_tictactoe_winner(game_id, winner_id):
    c.execute("""
    UPDATE tictactoe
    SET winner=?, ended=?
    WHERE game_id=?
    """, (winner_id, True, game_id))

    conn.commit()

def create_tictactoe(room_id, player_x, player_o):
    game_id = generate_id('tictactoe', 'game_id')

    c.execute("""
    INSERT INTO tictactoe
    VALUES(?, ?, ?, ?, '{"state": [["#", "#", "#"], ["#", "#", "#"], ["#", "#", "#"]]}', ?, NULL, false)
    """, (game_id, room_id, player_x, player_o, player_x if player_x != "" else player_o))
    conn.commit()

def list_tictactoes(room_id):
    c.execute("SELECT game_id, player_x, player_o, winner, ended FROM tictactoe WHERE room_id = ?", (room_id,))
    return c.fetchall()

def check_tictactoe_availability(game_id):
    c.execute("SELECT player_x, player_o FROM tictactoe WHERE game_id = ?", (game_id,))
    player_x, player_o = c.fetchone()
    if not player_x or not player_o:
        return True
    return False

def delete_all_tictactoes(room_id):
    c.execute("DELETE FROM tictactoe WHERE room_id = ?", (room_id,))
    conn.commit()
    return "deleted"

def delete_one_tictactoe(room_id, game_id):
    c.execute("DELETE FROM tictactoe WHERE room_id = ? AND game_id = ?", (room_id, game_id))
    conn.commit()
    return "game deleted"

def add_user_to_tictactoe(game_id, player, user_id):
    if player == "x":
        c.execute("UPDATE tictactoe SET player_x = ? WHERE game_id = ?", (user_id, game_id))
        print("x dodamo")
        conn.commit()
    elif player == "o":
        c.execute("UPDATE tictactoe SET player_o = ? WHERE game_id = ?", (user_id, game_id))
        print("o dodamo")
        conn.commit()
    else:
        return "error"

# def join_tictactoe(game_id, player):
#     if check_tictactoe_availability():
        