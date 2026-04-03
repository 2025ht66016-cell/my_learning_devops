# src/Aceestver.py
import sqlite3

# Default DB path (can be overridden in tests)
_DB_PATH = "aceest.db"

PROGRAMS = {
    "FL": {
        "code": "FL",
        "name": "Fat Loss",
        "summary": "High-intensity conditioning and a calorie-controlled nutrition plan.",
        "workout": "Mon: 5x5 Back Squat + AMRAP\nTue: EMOM 20min Assault Bike\nWed: Bench Press + 21-15-9\nThu: 10RFT Deadlifts/Box Jumps\nFri: 30min Active Recovery",
        "diet": "B: 3 Egg Whites + Oats Idli\nL: Grilled Chicken + Brown Rice\nD: Fish Curry + Millet Roti\nTarget: 2,000 kcal",
        "color": "#e74c3c",
        "calorie_factor": 22,
    },
    "MG": {
        "code": "MG",
        "name": "Muscle Gain",
        "summary": "Progressive strength blocks with a calorie-surplus meal plan.",
        "workout": "Mon: Squat 5x5\nTue: Bench 5x5\nWed: Deadlift 4x6\nThu: Front Squat 4x8\nFri: Incline Press 4x10\nSat: Barbell Rows 4x10",
        "diet": "B: 4 Eggs + PB Oats\nL: Chicken Biryani (250g Chicken)\nD: Mutton Curry + Jeera Rice\nTarget: 3,200 kcal",
        "color": "#2ecc71",
        "calorie_factor": 35,
    },
    "BG": {
        "code": "BG",
        "name": "Beginner",
        "summary": "Foundational conditioning for new members focused on form and consistency.",
        "workout": "Circuit Training: Air Squats, Ring Rows, Push-ups.\nFocus: Technique Mastery & Form (90% Threshold)",
        "diet": "Balanced Tamil Meals: Idli-Sambar, Rice-Dal, Chapati.\nProtein: 120g/day",
        "color": "#3498db",
        "calorie_factor": 26,
    },
}


# ── Business logic ───────────────────────────────────────────────

def get_program_by_code(program_code: str):
    """Lookup program by code (case-insensitive)."""
    if not program_code:
        return None
    return PROGRAMS.get(program_code.upper())


def get_programs_summary() -> list[dict]:
    """Return summary of all programs."""
    return [
        {
            "code": program["code"],
            "name": program["name"],
            "summary": program["summary"],
            "color": program["color"],
            "calorie_factor": program["calorie_factor"],
        }
        for program in PROGRAMS.values()
    ]


def calculate_calories(program_code: str, weight_kg: int):
    """Estimate calories based on program code and weight."""
    if weight_kg <= 0:
        return None
    program = get_program_by_code(program_code)
    if not program:
        return None
    return weight_kg * program["calorie_factor"]


# ── Database setup ───────────────────────────────────────────────

def init_db(path: str = None):
    """Initialize SQLite database with clients and progress tables."""
    global _DB_PATH
    if path:
        _DB_PATH = path

    conn = sqlite3.connect(_DB_PATH)
    cur = conn.cursor()

    # Clients table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            weight_kg INTEGER,
            program_code TEXT,
            adherence INTEGER
        )
    """)

    # Progress tracking table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT,
            adherence INTEGER,
            week TEXT
        )
    """)

    conn.commit()
    conn.close()
