from flask import Flask, jsonify, request
import os
import psycopg2

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database=os.environ.get("DB_NAME", "labdb"),
        user=os.environ.get("DB_USER", "labuser"),
        password=os.environ.get("DB_PASSWORD", "labpass")
    )

@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "ok", "message": "Lab 6 API is running!"})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})

@app.route("/items", methods=["GET"])
def get_items():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM items;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({"items": [{"id": r[0], "name": r[1]} for r in rows]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    name = data.get("name", "")
    if not name:
        return jsonify({"error": "name is required"}), 400
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO items (name) VALUES (%s) RETURNING id;", (name,))
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"id": new_id, "name": name}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
