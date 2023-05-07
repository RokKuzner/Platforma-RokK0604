import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

DEVICES = """
CREATE TABLE IF NOT EXISTS devices(
user TEXT UNIQUE,
device_id TEXT UNIQUE,
game_id TEXT
);
"""

demo_users = [str(x) for x in range(15)]

ADD_DEMO_DEVICE = """
INSERT INTO devices VALUES(
?,
?,
null
);
"""

ADD_DEMO_USER = """
INSERT INTO users VALUES(
?, ?, ?
)
"""
c.execute(DEVICES)
conn.commit()

for x in demo_users:
    c.execute(ADD_DEMO_USER, (x, f"{x}@{x}.si", x))
    c.execute(ADD_DEMO_DEVICE, (x, x))

conn.commit()
conn.close()
