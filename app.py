from flask import Flask, render_template, redirect
import sqlite3
import requests

app = Flask(__name__)

DATABASE = "quotes.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote TEXT NOT NULL,
            author TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM quotes ORDER BY id DESC")
    history = cursor.fetchall()

    conn.close()

    return render_template('index.html', history=history)

@app.route('/get_quote')
def get_quote():

    response = requests.get("https://api.quotable.io/random")
    data = response.json()

    quote = data['content']
    author = data['author']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO quotes (quote, author) VALUES (?, ?)",
        (quote, author)
    )

    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/health')
def health():
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
