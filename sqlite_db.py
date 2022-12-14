import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

db_url = str(os.getenv("DATABASE_URL"))


class DBHelper:

    def insert_message(self, message):
        conn = psycopg2.connect(db_url, sslmode="require")
        cur = conn.cursor()
        cur.execute(f"SELECT user_id FROM users WHERE user_id={message.from_user.id}")
        data = cur.fetchone()
        if data is None:  
            cur.execute("INSERT INTO users(user_id, user_name, message_t, last_message_date) VALUES(%s, %s, %s, %s)", (message.from_user.id, message.from_user.username, message.text, message.date))
            conn.commit()
        else:
            cur.execute("UPDATE users SET message_t = (%s), last_message_date = (%s), user_name = (%s)  WHERE user_id = (%s)", (message.text, message.date, message.from_user.username, message.from_user.id))
            conn.commit()


 
    def warning_message(*args):
        conn = psycopg2.connect(db_url, sslmode="require")
        cur = conn.cursor()
        cur.execute("SELECT users.user_name FROM users RIGHT JOIN chatuser USING(user_id) WHERE NOW()::date-last_message_date>6")
        row = cur.fetchall()
        conn.commit()
        mass = []
        for i in row:
            mass.append("@"+i[0])
        return mass
  
  
            
    def kick_member_query(*args):
        conn = psycopg2.connect(db_url, sslmode="require")
        cur = conn.cursor()
        cur.execute("SELECT chatuser.user_id FROM chatuser LEFT JOIN users USING(user_id) WHERE NOW()::date-last_message_date>9")
        row = cur.fetchall()
        conn.commit()
        mass = []
        for i in row:
            mass.append(i[0])
        return mass