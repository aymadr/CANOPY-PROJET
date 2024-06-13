from pynput import mouse
import sqlite3

def increment_counter():
    with sqlite3.connect('clicks_db.sqlite') as conn:
        curseur = conn.cursor()
        curseur.execute('UPDATE click_count SET count = count + 1')
        conn.commit()
        curseur.execute('SELECT count FROM click_count')
        count = curseur.fetchone()[0]
    print(f"nombre de clic: {count}")

def on_click(x, y, button, pressed):
    if pressed and button == mouse.Button.left:
        increment_counter()

def start_mouse_listener():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

if __name__ == '__main__':
    start_mouse_listener()
