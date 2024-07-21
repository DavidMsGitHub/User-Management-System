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


class User():
    def __init__(self):
        self.conn = connect_db()
        self.cursor = self.conn.cursor()
    def create(self, username, email, password, gender):
        self.cursor.execute("INSERT INTO users (username, email, password, gender) VALUES (?, ?, ?, ?)", (username,email,password,gender))
        self.conn.commit()
        self.conn.close()

    def delete(self, id):
        self.cursor.execute("DELETE FROM users WHERE id = ?",(id))
        self.conn.commit()
        self.conn.close()

    def get_info(self, id):
        self.cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
        user_data = self.cursor.fetchone()
        column_names = [description[0] for description in self.cursor.description]
        return dict(zip(column_names, user_data))



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
    user = User()
    return jsonify(user.get_info(id))



@app.route('/add_user', methods=["POST"])
def add_user():
    username = request.form["username"]
    password = request.form["password"]
    email = request.form["email"]
    gender = request.form["gender"]

    user = User()
    user.create(username, password, email, gender)
    return jsonify({"Success": "Successfuly created new user"})

@app.route('/remove-user', methods=["GET"])
def delete_user():
    id = request.args.get("id")
    user = User()
    user.delete(id)
    return jsonify({"Success":f"Successfuly removed user with id {id}"})

if __name__ == "__main__":
    app.run(debug=True)

