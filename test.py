import sqlite3
username = "gfgfg"
# password = "qwerty123"
# email = "giorgi@gmail.com"
gender = "female"


            #_______#_

query = "SELECT * FROM users WHERE 1=1"
params = ("male")
conn = sqlite3.connect("user_data.db")
cursor = conn.cursor()
try:
    if gender:
        query += f" AND gender = '{gender}'"
except:
    pass
try:
    if username:
        query += f" AND username = '{username}'"
except:
    pass

try:
    if email:
        query += f" AND email = '{email}'"
except:
    pass
try:
    if gender:
        query += f" AND gender = '{gender}'"
except:
    pass

male = "male"
# print(query)
cursor.execute(query)
gela = cursor.fetchall()
columns = [description[0] for description in cursor.description]
guasha = dict(zip(columns, gela))
print(guasha)