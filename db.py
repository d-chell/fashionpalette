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
# META FUNCS #
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
    return User(uid, "poopturd")

def loginauth(uid, password):
    realpassword = execute("SELECT password FROM users WHERE id=?", (uid,))[0][0]
    if password == realpassword:
        return True
    return False

def test_db():
    execute("INSERT INTO users (username, password) \
        VALUES ('dana', 'dope1')")
    execute("INSERT INTO users (username, password) \
        VALUES ('da', 'docwpe1')")
    execute("INSERT INTO users (username, password) \
        VALUES ('daddna', 'dow1')")

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
                `time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `color` INTEGER,
                `opinon` INTEGER,
                `comments` VARCHAR(255)
            );""")
