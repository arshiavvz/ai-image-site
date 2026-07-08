from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
import sqlite3

auth_bp = Blueprint("auth", __name__)

def get_db():
    return sqlite3.connect("database.db")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        password_hash = generate_password_hash(password)

        conn = get_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            conn.commit()

        except sqlite3.IntegrityError:
            conn.close()
            return "این نام کاربری قبلاً ثبت شده است."

        conn.close()

        return redirect(url_for("home"))

    return render_template("register.html")
