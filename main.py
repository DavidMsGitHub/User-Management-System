import sqlite3
from flask import Flask, request, jsonify

def connect_db():
    conn = sqlite3.connect('user_data.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users 
        (id INTEGER PRIMARY KEY, 
         username CONST NOT NULL,
         email TEXT NOT NULL,
         password TEXT NOT NULL,
         gender TEXT NOT NULL)''')
    return conn


# class User():
#     def __init__(self):
#         self.conn = connect_db()
#         self.cursor = self.conn.cursor()
#     def create(self, username, email, password, gender):
#         self.cursor.execute("INSERT INTO users (username, email, password, gender) VALUES (?, ?, ?, ?)", (username,email,password,gender))
#         self.conn.commit()
#         self.conn.close()
#
#     def delete(self, id):
#         self.cursor.execute("DELETE FROM users WHERE id = ?",(id))
#         self.conn.commit()
#         self.conn.close()
#
#     def get_info(self, id):
#         self.cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
#         user_data = self.cursor.fetchone()
#         column_names = [description[0] for description in self.cursor.description]
#         return dict(zip(column_names, user_data))
#
#     def search_name(self, name):
#         self.cursor.execute("SELECT * FROM users WHERE username LIKE ?", (f"{name}%",))
#         users = self.cursor.fetchall()
#         columns = [description[0] for description in self.cursor.description]
#         return [dict(zip(columns, i)) for i in users]





#--#__#_#_#__#_#_#___3-3-3-#_3-3-_#_#-g


app = Flask(__name__)

@app.route('/all_users')
def all_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    all_users = [dict(zip(columns, i)) for i in users]
    conn.close()
    return jsonify(all_users)

@app.route('/user/<id>')
def check_user(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
    user_info = cursor.fetchone()
    column_names = [description[0] for description in cursor.description]
    user_data = dict(zip(column_names, user_info))
    return jsonify(user_data)

@app.route("/search", methods=["GET"])
def search_by_name():
    name_to_find = request.args.get("name")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username LIKE ?", (f"%{name_to_find}%",))
    users = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    conn.close()
    return jsonify([dict(zip(columns, i)) for i in users])


@app.route('/add_user', methods=["POST"])
def add_user():
    username = request.form["username"]
    password = request.form["password"]
    email = request.form["email"]
    gender = request.form["gender"]
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, email, password, gender) VALUES (?, ?, ?, ?)",
                        (username, email, password, gender))
    conn.commit()
    conn.close()
    return jsonify({"Success": "Successfuly created new user"})

@app.route('/remove-user', methods=["GET", "DELETE"])
def delete_user():
    conn = connect_db()
    cursor = conn.cursor()
    id_to_remove = request.args.get("id")
    cursor.execute("DELETE FROM users WHERE id = ?", (id_to_remove,))
    conn.commit()
    conn.close()
    return jsonify({"Success":f"Successfuly removed user with id {id_to_remove}"})

if __name__ == "__main__":
    app.run(debug=True)