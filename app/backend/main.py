
import os
import time

import psycopg
from flask import Flask, jsonify

app = Flask(__name__)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "ecommerce"),
    "user": os.getenv("DB_USER", "ecommerce_user"),
    "password": os.getenv("DB_PASSWORD", "local_dev_password"),
}

SAMPLE_PRODUCTS = [
    ("Laptop", 55000),
    ("Headphones", 2500),
    ("Keyboard", 1500),
]


def get_connection():
    return psycopg.connect(**DB_CONFIG)


def initialize_database():
    for attempt in range(10):
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS products (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(100) NOT NULL,
                            price NUMERIC(10, 2) NOT NULL
                                CHECK (price >= 0)
                        )
                    """)

                    cur.execute("SELECT COUNT(*) FROM products")
                    count = cur.fetchone()[0]

                    if count == 0:
                        cur.executemany(
                            "INSERT INTO products (name, price) VALUES (%s, %s)",
                            SAMPLE_PRODUCTS,
                        )
            return
        except psycopg.OperationalError:
            if attempt == 9:
                raise
            time.sleep(2)


@app.route("/")
def home():
    return jsonify({
        "application": "E-Commerce API",
        "version": "1.0.0",
        "status": "running",
    })


@app.route("/health")
def health():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except psycopg.Error:
        return jsonify({"status": "unhealthy", "database": "disconnected"}), 503


@app.route("/api/products")
def get_products():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, name, price FROM products ORDER BY id"
                )
                rows = cur.fetchall()

        products = [
            {"id": row[0], "name": row[1], "price": float(row[2])}
            for row in rows
        ]
        return jsonify(products), 200
    except psycopg.Error:
        return jsonify({"error": "Database unavailable"}), 503


if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=5000, debug=False)
