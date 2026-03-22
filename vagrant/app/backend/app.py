from flask import Flask
import os
import socket
import psycopg2

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "devops")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "devops123")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def ensure_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id SERIAL PRIMARY KEY,
            hostname TEXT
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


@app.route("/")
def home():
    hostname = socket.gethostname()
    ensure_table()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO visits (hostname) VALUES (%s)", (hostname,))
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM visits")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()

    return {
        "message": "DevOps portfolio project with PostgreSQL!",
        "hostname": hostname,
        "visits": count
    }


@app.route("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
