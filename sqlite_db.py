import psycopg2
from config import *


class DBHelper:

    def insert_message(self, message):
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cur = conn.cursor()
        cur.execute(f'SELECT user_id FROM users WHERE user_id={message.from_user.id}')
        data = cur.fetchone()
        if data is None:  
            cur.execute(f'INSERT INTO users VALUES("{message.from_user.id}", "{message.from_user.username}", "{message.text}", "{message.date}")')
            conn.commit()
        else:
            cur.execute("UPDATE users SET last_message = ?, last_message_date = ? WHERE user_id = ? ", (message.text, message.date, message.from_user.id))
            conn.commit()


 
    def warning_message(*args):
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cur = conn.cursor()
        cur.execute("SELECT chatuser.user_name, strftime('%d-%m-%Y', 'now')-strftime('%d-%m-%Y', last_message_date) AS day FROM chatuser LEFT JOIN users USING(user_id) WHERE day>6")
        row = cur.fetchall()
        conn.commit()
        mass = []
        for i in row:
            mass.append("@"+i[0])
        return mass
  
  
            
    def kick_member_query(*args):
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cur = conn.cursor()
        cur.execute("SELECT chatuser.user_id, strftime('%d-%m-%Y', 'now')-strftime('%d-%m-%Y', last_message_date) AS day FROM chatuser LEFT JOIN users USING(user_id) WHERE day>9")
        row = cur.fetchall()
        conn.commit()
        mass = []
        for i in row:
            mass.append(i[0])
        return mass