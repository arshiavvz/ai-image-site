from flask import Flask, render_template, request
import urllib.parse
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("database.db")

@app.route("/")
def home():
    return render_template("index.html", image_url=None)

@app.route("/generate", methods=["POST"])
def generate():
    prompt = request.form["prompt"]

    image_url = "https://image.pollinations.ai/prompt/" + urllib.parse.quote(prompt)

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO images (prompt, image_url) VALUES (?, ?)",
        (prompt, image_url)
    )

    conn.commit()
    conn.close()

    return render_template(
        "index.html",
        image_url=image_url,
        prompt=prompt
    )
@app.route("/gallery")
def gallery():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT prompt, image_url FROM images ORDER BY id DESC"
    )

    rows = cursor.fetchall()
    conn.close()

    images = []

    for row in rows:
        images.append({
            "prompt": row[0],
            "image": row[1]
        })

    return render_template(
        "gallery.html",
        images=images
    )

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
