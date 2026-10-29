from flask import Flask, render_template, request
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


def create_table():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return "My Authentication Project Started!"


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                (name, email, password)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "This email is already registered. Please use another email."

        conn.close()
        return f"Signup successful! Welcome, {name}"

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT name, password_hash FROM users WHERE email = ?",
            (email,)
        )

        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[1], password):
            return f"Login successful! Welcome, {user[0]}"

        return "Invalid email or password!"

    return render_template("login.html")


if __name__ == "__main__":
    create_table()
    app.run(debug=True)