# app.py
from flask import Flask, render_template, jsonify, redirect, url_for
from dotenv import load_dotenv
import os
from pynput import mouse
import sqlite3

load_dotenv()

app = Flask('__name__')


def init_db():

    conn = sqlite3.connect("clicks_db.sqlite")
    curseur = conn.cursor()

    curseur.execute('''
        CREATE TABLE IF NOT EXISTS click_count (
            id INTEGER PRIMARY KEY,
            count INTEGER NOT NULL
        )
    ''')

    curseur.execute('SELECT count(*) FROM click_count')
    if curseur.fetchone()[0] == 0:
        curseur.execute('INSERT INTO click_count (count) VALUES (0)')
    conn.commit()
    conn.close()

def increment_counter():
    conn = sqlite3.connect('clicks_db.sqlite')
    curseur = conn.cursor()
    curseur.execute('UPDATE click_count SET count = count + 1')
    conn.commit()
    curseur.execute('SELECT count FROM click_count')
    count = curseur.fetchone()[0]
    conn.close()
    return count

def reset():
    conn = sqlite3.connect('clicks_db.sqlite')
    curseur = conn.cursor()
    curseur.execute('UPDATE click_count SET count = 0')
    conn.commit()
    conn.close

init_db()
reset()

def on_click(x, y, button, pressed):
    if pressed and button == mouse.Button.left:
        increment_counter()
 

@app.route('/')
def home():
    return render_template('index.html')



##@app.route('/increment', methods=['POST'])
##def increment():
  ##  count = increment_counter()
    ##return jsonify(count=count)


@app.route('/count', methods=['GET'])
def count():
    conn = sqlite3.connect('clicks_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT count FROM click_count')
    count = cursor.fetchone()[0]
    conn.close()
    return jsonify(count=count)




if __name__ == '__main__':
    app.run(debug=True) 

