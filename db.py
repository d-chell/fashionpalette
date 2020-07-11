import sqlite3 as sql
import re
import time
import bcrypt
import base64
from flask_login import UserMixin
from datetime import datetime, timedelta

# Database name
db = "fp.db"

#######################
# DB HELPER FUNCTIONS #
#######################

def execute(cmd, values=None, one=False):
    with sql.connect(db) as conn:
        cur = conn.cursor()
        if values:
            cur.execute(cmd, values)
        else:
            cur.execute(cmd)
        if one:
            return cur.fetchone()
        else:
            return cur.fetchall()

##############
# USER FUNCS #
##############

class User(UserMixin):
    def __init__(self, uid, name):
        self.id = uid
        self.name = name

    def get_id(self):
        return self.id

def get_uid(username):
    return execute("SELECT id FROM users WHERE username=?", \
                  (username,))[0][0]

def find_user(uid):
    user_data = execute("SELECT * FROM users WHERE id=?", (uid,))
    if not user_data:
        return User(uid, "unreal")
    return User(uid, user_data[0][1])

def login_auth(uid, password):
    passwhash = execute("SELECT password FROM users WHERE id=?", (uid,))[0][0]
    return bcrypt.checkpw(password, passwhash)

def create_user(username, password):
    execute("INSERT INTO users (username, password) \
        VALUES (?, ?)", (username, password))

################
# History Logs #
################

def create_log(uid, date, color, opinion, comments):
    execute("INSERT INTO history (id, date, color, opinion, comments) \
        VALUES (?, ?, ?, ?, ?)", (uid, date, color, opinion, comments))

def get_history(uid):
    logs = execute("SELECT * FROM history WHERE id=?", (uid,))
    if not logs:
        return [()]
    return logs

def delete_log(hid):
    execute("DELETE FROM history WHERE hid=?", (hid,))
    print(hid)

#################
# FASHION FUNCS #
#################

def store_profile(uid, profile):
    execute("UPDATE users SET profile=? WHERE id=?", (profile, uid))

def get_profile(uid):
    profile = execute("SELECT profile FROM users WHERE id=?", (uid,))
    try:
        if not profile[0][0]:
            with open("static/defaultprofile.jpg", 'rb') as f:
                base64file = base64.b64encode(f.read())
                base64file = base64file.decode("ascii")
            return base64file
    except:
        with open("static/defaultprofile.jpg") as f:
            base64file = base64.b64encode(f.read())
            base64file = base64file.decode("ascii")
        return base64file
    return profile[0][0]

def store_palette(uid, skin, eyes, hair):
    print(uid, skin, eyes, hair)
    execute("UPDATE users SET skin=?, eyes=?, hair=? WHERE id=?", (skin, eyes, hair, uid))

def get_palette(uid):
    palette = execute("SELECT skin, eyes, hair FROM users WHERE id=?", (uid,))
    try:
        if not palette[0][0]:
            return None
    except:
        return None
    return palette[0][0], palette[0][1], palette[0][2]


def validate_alphanum(string):
    if re.compile("^[a-zA-Z0-9-]+$").match(string):
        return True
    return False

def reset():
    execute("DROP TABLE IF EXISTS `users`;")
    execute("""CREATE TABLE `users` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `profile` VARCHAR(16777216),
                `username` VARCHAR(255),
                `password` CHAR(60),
                `skin` INTEGER,
                `hair` INTEGER,
                `eyes` INTEGER
            );""")
    execute("DROP TABLE IF EXISTS `history`;")
    execute("""CREATE TABLE `history` (
                `hid` INTEGER PRIMARY KEY AUTOINCREMENT,
                `id` INTEGER,
                `date` TIMESTAMP,
                `color` INTEGER,
                `opinion` INTEGER,
                `comments` VARCHAR(255)
            );""")
