
PROGRAMS = {
    "FL": {
        "code": "FL",
        "name": "Fat Loss",
        "summary": "High-intensity conditioning and a calorie-controlled nutrition plan.",
        "workout": "Mon: 5x5 Back Squat + AMRAP\nTue: EMOM 20min Assault Bike\nWed: Bench Press + 21-15-9\nThu: 10RFT Deadlifts/Box Jumps\nFri: 30min Active Recovery",
        "diet": "B: 3 Egg Whites + Oats Idli\nL: Grilled Chicken + Brown Rice\nD: Fish Curry + Millet Roti\nTarget: 2,000 kcal",
        "color": "#e74c3c",
    },
    "MG": {
        "code": "MG",
        "name": "Muscle Gain",
        "summary": "Progressive strength blocks with a calorie-surplus meal plan.",
        "workout": "Mon: Squat 5x5\nTue: Bench 5x5\nWed: Deadlift 4x6\nThu: Front Squat 4x8\nFri: Incline Press 4x10\nSat: Barbell Rows 4x10",
        "diet": "B: 4 Eggs + PB Oats\nL: Chicken Biryani (250g Chicken)\nD: Mutton Curry + Jeera Rice\nTarget: 3,200 kcal",
        "color": "#2ecc71",
    },
    "BG": {
        "code": "BG",
        "name": "Beginner",
        "summary": "Foundational conditioning for new members focused on form and consistency.",
        "workout": "Circuit Training: Air Squats, Ring Rows, Push-ups.\nFocus: Technique Mastery & Form (90% Threshold)",
        "diet": "Balanced Tamil Meals: Idli-Sambar, Rice-Dal, Chapati.\nProtein: 120g/day",
        "color": "#3498db",
    },
}


def get_program_by_code(program_code: str):
    return PROGRAMS.get(program_code.upper())


def get_programs_summary() -> list[dict[str, str]]:
    return [
        {
            "code": program["code"],
            "name": program["name"],
            "summary": program["summary"],
            "color": program["color"],
        }
        for program in PROGRAMS.values()
    ]
