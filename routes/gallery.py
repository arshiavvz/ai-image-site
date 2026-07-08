from flask import Blueprint, render_template
import sqlite3

gallery_bp = Blueprint("gallery", __name__)

DATABASE = "database.db"


def get_db():
    return sqlite3.connect(DATABASE)


@gallery_bp.route("/gallery")
def gallery():

    conn = get_db()
    cursor = conn.cursor()

    # فعلاً کاربر شماره 1
    # بعداً از Flask-Login می‌گیریم
    user_id = 1

    cursor.execute(
        """
        SELECT id, prompt, image_url
        FROM images
        WHERE user_id=?
        ORDER BY id DESC
        """,
        (user_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    images = []

    for row in rows:

        images.append({
            "id": row[0],
            "prompt": row[1],
            "image": row[2]
        })

    return render_template(
        "gallery.html",
        images=images
    )
