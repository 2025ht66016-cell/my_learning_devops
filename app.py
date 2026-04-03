
from flask import Flask, jsonify, render_template_string

from src.Aceestver import get_program_by_code, get_programs_summary


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index() -> str:
        programs = get_programs_summary()
        return render_template_string(
            """
            <!doctype html>
            <html lang="en">
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>ACEest Fitness & Gym</title>
                <style>
                    :root {
                        --bg: #0e1116;
                        --panel: #171b22;
                        --accent: #d4af37;
                        --text: #f5f5f5;
                        --muted: #a7acb8;
                    }
                    * { box-sizing: border-box; }
                    body {
                        margin: 0;
                        font-family: Helvetica, Arial, sans-serif;
                        background: radial-gradient(circle at top, #1f2630 0%, var(--bg) 60%);
                        color: var(--text);
                    }
                    main {
                        max-width: 1040px;
                        margin: 0 auto;
                        padding: 40px 20px 64px;
                    }
                    .hero {
                        margin-bottom: 24px;
                        padding: 24px;
                        border: 1px solid rgba(212, 175, 55, 0.25);
                        border-radius: 18px;
                        background: rgba(23, 27, 34, 0.95);
                    }
                    .hero h1 {
                        margin: 0 0 8px;
                        color: var(--accent);
                    }
                    .hero p {
                        margin: 0;
                        color: var(--muted);
                        line-height: 1.5;
                    }
                    .grid {
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
                        gap: 18px;
                        margin-top: 24px;
                    }
                    .card {
                        padding: 18px;
                        border-radius: 16px;
                        background: var(--panel);
                        border-top: 4px solid var(--accent-color);
                        box-shadow: 0 14px 35px rgba(0, 0, 0, 0.24);
                    }
                    .card h2 {
                        margin: 0 0 8px;
                        font-size: 1.1rem;
                    }
                    .badge {
                        display: inline-block;
                        margin-bottom: 12px;
                        padding: 4px 10px;
                        border-radius: 999px;
                        background: rgba(255, 255, 255, 0.08);
                        color: var(--muted);
                        font-size: 0.85rem;
                    }
                    code {
                        color: var(--accent);
                    }
                </style>
            </head>
            <body>
                <main>
                    <section class="hero">
                        <h1>ACEest Fitness & Gym</h1>
                        <p>
                            Release 1.0 exposes the core training programs for Fat Loss, Muscle Gain,
                            and Beginner onboarding. Use the API endpoints <code>/api/programs</code>
                            and <code>/api/programs/&lt;code&gt;</code> for automation or integration.
                        </p>
                    </section>
                    <section class="grid">
                        {% for program in programs %}
                        <article class="card" style="--accent-color: {{ program.color }};">
                            <span class="badge">{{ program.code }}</span>
                            <h2>{{ program.name }}</h2>
                            <p>{{ program.summary }}</p>
                        </article>
                        {% endfor %}
                    </section>
                </main>
            </body>
            </html>
            """,
            programs=programs,
        )

    @app.get("/health")
    def health() -> tuple:
        return jsonify({"service": "aceest-fitness", "status": "ok"}), 200

    @app.get("/api/programs")
    def list_programs() -> tuple:
        return jsonify({"programs": get_programs_summary()}), 200

    @app.get("/api/programs/<program_code>")
    def get_program(program_code: str) -> tuple:
        program = get_program_by_code(program_code)
        if program is None:
            return jsonify({"error": f"Program '{program_code}' was not found."}), 404
        return jsonify(program), 200

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=False)
