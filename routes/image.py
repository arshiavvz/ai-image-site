from flask import Blueprint, render_template, request
import urllib.parse
import sqlite3

image_bp = Blueprint("image", __name__)

DATABASE = "database.db"


def get_db():
    return sqlite3.connect(DATABASE)


@image_bp.route("/")
def home():
    return render_template(
        "index.html",
        image_url=None
    )


@image_bp.route("/generate", methods=["POST"])
def generate():

    prompt = request.form["prompt"]

    image_url = (
        "https://image.pollinations.ai/prompt/"
        + urllib.parse.quote(prompt)
    )

    conn = get_db()
    cursor = conn.cursor()

    # فعلاً مقدار user_id ثابت است.
    # بعد از اضافه شدن سیستم ورود،
    # این مقدار از کاربر لاگین‌کرده گرفته می‌شود.
    user_id = 1

    cursor.execute(
        """
        INSERT INTO images
        (user_id, prompt, image_url)
        VALUES (?, ?, ?)
        """,
        (
            user_id,
            prompt,
            image_url
        )
    )

    conn.commit()
    conn.close()

    return render_template(
        "index.html",
        image_url=image_url,
        prompt=prompt
    )
