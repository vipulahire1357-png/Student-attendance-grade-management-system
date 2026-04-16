"""
setup_db.py  — Run once to initialise the database.
Creates 'attendance_db', applies schema.sql, then loads sample_data.sql.
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("DB_HOST", "localhost")
PORT = os.getenv("DB_PORT", "5432")
USER = os.getenv("DB_USER", "postgres")
PWD  = os.getenv("DB_PASSWORD", "")
DB   = os.getenv("DB_NAME", "attendance_db")

BASE = os.path.dirname(os.path.abspath(__file__))


def connect(dbname="postgres"):
    return psycopg2.connect(host=HOST, port=PORT, dbname=dbname,
                            user=USER, password=PWD)


def create_database():
    conn = connect("postgres")
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB,))
    if cur.fetchone():
        print(f"[OK] Database '{DB}' already exists.")
    else:
        cur.execute(f'CREATE DATABASE "{DB}"')
        print(f"[OK] Database '{DB}' created.")
    conn.close()


def run_sql_file(path, label):
    with open(path, "r", encoding="utf-8") as f:
        sql = f.read()
    conn = connect(DB)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(sql)
    conn.close()
    print(f"[OK] {label} applied.")


if __name__ == "__main__":
    print("=== SAGMS Database Setup ===")
    create_database()
    run_sql_file(os.path.join(BASE, "schema.sql"),      "schema.sql")
    run_sql_file(os.path.join(BASE, "sample_data.sql"), "sample_data.sql")
    print("\n✓ Setup complete! Run:  python app.py")
