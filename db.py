import sqlite3 as sql
import re
import time
import bcrypt
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
    print(user_data)
    if not user_data:
        return User(uid, "unreal")
    return User(uid, user_data[0][1])

def login_auth(uid, password):
    passwhash = execute("SELECT password FROM users WHERE id=?", (uid,))[0][0]
    print(passwhash, password)
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

##############
# TIME FUNCS #
##############

simple_time_format = "%H:%M:%S"

def print_time(time_obj):
    return time_obj.strftime(simple_time_format)

def validate_alphanum(string):
    if re.compile("^[a-zA-Z0-9-]+$").match(string):
        return True
    return False

def reset():
    execute("DROP TABLE IF EXISTS `users`;")
    execute("""CREATE TABLE `users` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `username` VARCHAR(255),
                `password` CHAR(60),
                `skin` VARCHAR(255),
                `hair` VARCHAR(255),
                `eyes` VARCHAR(255)
            );""")
    execute("DROP TABLE IF EXISTS `history`;")
    execute("""CREATE TABLE `history` (
                `id` INTEGER,
                `date` TIMESTAMP,
                `color` INTEGER,
                `opinion` INTEGER,
                `comments` VARCHAR(255)
            );""")
