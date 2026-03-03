import sqlite3
import json
import os

class Database:
    def __init__(self, db_path='/home/ubuntu/telegram_bot/home/ubuntu/project_review/bot_database.db'):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # جدول الحسابات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone TEXT UNIQUE,
                    api_id INTEGER,
                    api_hash TEXT,
                    session_name TEXT,
                    role TEXT, -- 'worker' (تحليل ونقل) or 'advertiser' (نشر إعلانات)
                    status TEXT DEFAULT 'inactive'
                )
            ''')
            # جدول المهام (للإعلانات)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ad_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message TEXT,
                    target_groups TEXT, -- JSON list of group IDs/usernames
                    interval_minutes INTEGER,
                    last_run TIMESTAMP,
                    status TEXT DEFAULT 'active'
                )
            ''')
            # جدول الكلمات المفتاحية المخصصة
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS custom_keywords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    keyword TEXT UNIQUE
                )
            ''')
            # جدول الإعدادات العامة
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            ''')
            conn.commit()

    # عمليات الحسابات
    def add_account(self, phone, api_id, api_hash, session_name, role):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO accounts (phone, api_id, api_hash, session_name, role) VALUES (?, ?, ?, ?, ?)',
                             (phone, api_id, api_hash, session_name, role))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False

    def remove_account(self, phone):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM accounts WHERE phone = ?', (phone,))
            conn.commit()

    def get_accounts(self, role=None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if role:
                cursor.execute('SELECT * FROM accounts WHERE role = ?', (role,))
            else:
                cursor.execute('SELECT * FROM accounts')
            return cursor.fetchall()

    # عمليات الكلمات المفتاحية
    def add_keyword(self, keyword):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO custom_keywords (keyword) VALUES (?)', (keyword,))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False

    def get_keywords(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT keyword FROM custom_keywords')
            return [row[0] for row in cursor.fetchall()]

    # عمليات الإعلانات
    def add_ad_task(self, message, target_groups, interval_minutes):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO ad_tasks (message, target_groups, interval_minutes) VALUES (?, ?, ?)',
                         (message, json.dumps(target_groups), interval_minutes))
            conn.commit()

    def get_ad_tasks(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM ad_tasks WHERE status = "active"')
            return cursor.fetchall()
