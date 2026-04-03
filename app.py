import csv, io, sqlite3
import matplotlib.pyplot as plt
from flask import Flask, jsonify, request, Response
from src.Aceestver import (
    get_program_by_code,
    get_programs_summary,
    calculate_calories,
    init_db,
    _DB_PATH,
)

def create_app(db_path=None):
    app = Flask(__name__)
    init_db(db_path)

    # --- existing endpoints (health, programs, calories) ---

    @app.post("/api/clients")
    def add_client():
        data = request.get_json() or {}
        name, age, weight, program_code, adherence = (
            data.get("name"),
            data.get("age"),
            data.get("weight_kg"),
            data.get("program_code"),
            data.get("adherence"),
        )
        if not all([name, age, weight, program_code, adherence]):
            return jsonify({"error": "Missing fields"}), 400
        if not get_program_by_code(program_code):
            return jsonify({"error": "Program not found"}), 404

        conn = sqlite3.connect(_DB_PATH)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO clients (name, age, weight_kg, program_code, adherence) VALUES (?, ?, ?, ?, ?)",
            (name, age, weight, program_code, adherence),
        )
        conn.commit()
        conn.close()
        return jsonify(data), 201

    @app.get("/api/clients")
    def list_clients():
        conn = sqlite3.connect(_DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT name, age, weight_kg, program_code, adherence FROM clients")
        rows = cur.fetchall()
        conn.close()
        clients = [
            {"name": r[0], "age": r[1], "weight_kg": r[2], "program_code": r[3], "adherence": r[4]}
            for r in rows
        ]
        return jsonify({"total": len(clients), "clients": clients}), 200

    @app.get("/api/clients/export.csv")
    def export_csv():
        conn = sqlite3.connect(_DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT name, age, weight_kg, program_code, adherence FROM clients")
        rows = cur.fetchall()
        conn.close()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["name", "age", "weight_kg", "program_code", "adherence"])
        writer.writerows(rows)
        return Response(output.getvalue(), mimetype="text/csv")

    @app.get("/api/chart")
    def chart():
        conn = sqlite3.connect(_DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT name, adherence FROM clients")
        rows = cur.fetchall()
        conn.close()
        if not rows:
            return jsonify({"error": "No clients"}), 404

        names = [r[0] for r in rows]
        adherence = [r[1] for r in rows]

        fig, ax = plt.subplots()
        ax.bar(names, adherence)
        ax.set_ylabel("Adherence %")
        ax.set_title("Client Adherence Chart")

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        return Response(buf.getvalue(), mimetype="image/png")

    @app.post("/api/progress")
    def log_progress():
        data = request.get_json() or {}
        client_name, adherence, week = (
            data.get("client_name"),
            data.get("adherence"),
            data.get("week"),
        )
        if not all([client_name, adherence, week]):
            return jsonify({"error": "Missing fields"}), 400

        conn = sqlite3.connect(_DB_PATH)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO progress (client_name, adherence, week) VALUES (?, ?, ?)",
            (client_name, adherence, week),
        )
        conn.commit()
        conn.close()
        return jsonify(data), 201

    @app.get("/api/progress/<client_name>")
    def get_progress(client_name):
        conn = sqlite3.connect(_DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT adherence, week FROM progress WHERE client_name=?", (client_name,))
        rows = cur.fetchall()
        conn.close()
        sessions = [{"adherence": r[0], "week": r[1]} for r in rows]
        return jsonify({"total": len(sessions), "sessions": sessions}), 200

    return app
