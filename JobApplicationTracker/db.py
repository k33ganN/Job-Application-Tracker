import sqlite3
import csv
from datetime import datetime

DB_NAME = "applications.db"

# Database Setup

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    with get_connection() as conn :
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                role TEXT NOT NULL,
                date_applied TEXT NOT NULL,
                status TEXT NOT NULL,
                notes TEXT
            )
            """ 
        )
        conn.commit()

# CRUD Operations
def add_application(company, role, date_applied, status="applied", notes=""):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO applications (company, role, date_applied, status, notes) 
            VALUES (?,?,?,?,?)
            """,
            (company, role, date_applied, status, notes),
         )
        conn.commit()

def list_applications(status_filter=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        if status_filter:
            cursor.execute("SELECT * FROM applications WHERE status = ?", (status_filter,))
        else:
            cursor.execute("SELECT * FROM applications")
        return cursor.fetchall()

def update_status(app_id, new_status):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE applications SET status = ? WHERE id = ?",
            (new_status, app_id),
         )
        conn.commit()

def update_notes(app_id, notes):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE applications SET notes = ? WHERE id = ?",
            (notes, app_id),
        )
        conn.commit()

def update_application(app_id, company, role, status):
    with get_connection() as conn:
        cursor=conn.cursor()
        cursor.execute("""
            UPDATE applications
            SET company = ?, role = ?, status = ?
            WHERE id = ?
        """, (company, role, status, app_id))
        conn.commit()

def delete_application(app_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM applications WHERE id = ?", (app_id,))
        conn.commit()

# EXPORT

def export_to_csv(filename="applications.csv"):
    rows = list_applications()
    headers = ["id", "company", "role", "date_applied", "status", "notes"]

    with open(filename, "w", newline="", encoding ="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
