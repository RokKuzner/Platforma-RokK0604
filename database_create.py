import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

USERS = """
CREATE TABLE IF NOT EXISTS users(
username TEXT UNIQUE,
email TEXT UNIQUE,
password TEXT
)
"""

ROOMS = """
CREATE TABLE IF NOT EXISTS rooms(
id TEXT UNIQUE,
name TEXT,
room_owner TEXT,
date_created TEXT
)
"""

USER_IN_ROOM = """
CREATE TABLE IF NOT EXISTS user_in_room(
room_id TEXT,
username TEXT
)
"""

MESSAGES = """
CREATE TABLE IF NOT EXISTS messages(
username TEXT,
text TEXT,
room_id TEXT,
date TEXT
)
"""

TICTACTOE = """
CREATE TABLE IF NOT EXISTS tictactoe(
game_id TEXT,
room_id TEXT,
player_x TEXT,
player_o TEXT,
state TEXT,
next_player TEXT,
winner TEXT,
ended BOOLEAN
)
"""
c.execute(TICTACTOE)

ADD_DEMO_TICTACTOE = """
INSERT INTO tictactoe VALUES("tictactoe_2", "abc123", "miha", "test", '{"state": [["#", "#", "#"], ["#", "#", "#"], ["#", "#", "#"]]}', "miha", NULL, false)
"""
c.execute(ADD_DEMO_TICTACTOE)

ADD_DEMO_MESSAGE = """
INSERT INTO messages VALUES("test", "Moje sporočilo", "9860", "2023-01-01")
"""

ADD_DEMO_ROOM = """
INSERT INTO rooms VALUES(
"abc123", "ime sobe", "miha","2022-11-16"
)
"""

ADD_DEMO_USER = """
INSERT INTO users VALUES(
"miha", "miha@404.si", "miha1234"
)
"""

ADD_USER_INTO_ROOM = """
INSERT INTO user_in_room VALUES(
"abc123", "miha"
)
"""

c.execute(USERS)
c.execute(ROOMS)
c.execute(USER_IN_ROOM)
c.execute(MESSAGES)
#c.execute(ADD_DEMO_USER)
# c.execute(ADD_DEMO_ROOM)
#c.execute(ADD_USER_INTO_ROOM)
# c.execute(ADD_DEMO_MESSAGE)

# Ne pozabimo v bazo podatke shraniti
# in povezavo do baze zapreti.
conn.commit()
conn.close()
