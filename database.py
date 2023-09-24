# database.py
import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self, db_name='appointments.db'):
        self.db_name = db_name
        self.conn = self.connect_db()
        self.create_table()

    def connect_db(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                appointment_date TEXT NOT NULL,
                num_appointments INTEGER,
                server_response_time REAL
            )
        ''')
        self.conn.commit()

    def fetch_last_entry(self):
        c = self.conn.cursor()
        c.execute('''
            SELECT * FROM appointments ORDER BY id DESC LIMIT 1
        ''')
        row = c.fetchone()
        return row

    def insert_data(self, appointment_date, server_response_time, num_appointments=None):
        c = self.conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute('''
            INSERT INTO appointments (timestamp, appointment_date, num_appointments, server_response_time)
            VALUES (?, ?, ?, ?)
        ''', (now, appointment_date, num_appointments, server_response_time))
        self.conn.commit()

    def close(self):
        self.conn.close()
