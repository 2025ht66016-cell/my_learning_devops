# app.py
from flask import Flask, jsonify, request
from src.Aceestver import (
    get_program_by_code,
    get_programs_summary,
    calculate_calories,
    init_db,
)

def create_app(db_path=None):
    app = Flask(__name__)

    # Initialize database with provided path
    init_db(db_path)

    @app.route("/health")
    def health():
        return jsonify({"service": "aceest-fitness", "status": "ok"}), 200

    @app.route("/api/programs")
    def list_programs():
        return jsonify({"programs": get_programs_summary()}), 200

    @app.route("/api/programs/<program_code>")
    def get_program(program_code: str):
        program = get_program_by_code(program_code)
        if program is None:
            return jsonify({"error": f"Program '{program_code}' was not found."}), 404
        return jsonify(program), 200

    @app.route("/api/calories", methods=["POST"])
    def calories():
        data = request.get_json() or {}
        code = data.get("program_code")
        weight = data.get("weight_kg")
        if not code or not weight:
            return jsonify({"error": "Missing fields"}), 400
        result = calculate_calories(code, weight)
        if result is None:
            return jsonify({"error": "Program not found"}), 404
        return jsonify({"program_code": code, "estimated_calories": result}), 200

    return app

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=False)
