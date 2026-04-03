
import os
import tempfile

import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from app import create_app
from src.Aceestver import (calculate_calories, get_program_by_code,
                            get_programs_summary, init_db)



# ── business logic ────────────────────────────────────────────────────────────

def test_program_lookup_is_case_insensitive():
    program = get_program_by_code("fl")
    assert program is not None
    assert program["name"] == "Fat Loss"


def test_program_summary_exposes_three_profiles():
    summaries = get_programs_summary()
    assert len(summaries) == 3
    assert {p["code"] for p in summaries} == {"FL", "MG", "BG"}


def test_program_summary_includes_calorie_factor():
    summaries = get_programs_summary()
    for p in summaries:
        assert "calorie_factor" in p
        assert p["calorie_factor"] > 0


def test_unknown_program_code_returns_none():
    assert get_program_by_code("XX") is None


@pytest.mark.parametrize("code,weight,expected", [
    ("FL", 70, 70 * 22),
    ("MG", 80, 80 * 35),
    ("BG", 60, 60 * 26),
])
def test_calculate_calories(code, weight, expected):
    assert calculate_calories(code, weight) == expected


def test_calculate_calories_unknown_program_returns_none():
    assert calculate_calories("XX", 70) is None


def test_calculate_calories_zero_weight_returns_none():
    assert calculate_calories("FL", 0) is None


# ── API endpoints ─────────────────────────────────────────────────────────────

@pytest.fixture
def client(tmp_db):
    return create_app(db_path=tmp_db).test_client()


def test_health_endpoint_returns_ok_status(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"service": "aceest-fitness", "status": "ok"}


def test_program_list_endpoint_returns_expected_payload(client):
    response = client.get("/api/programs")
    payload = response.get_json()
    assert response.status_code == 200
    assert len(payload["programs"]) == 3


def test_program_detail_endpoint_returns_program_data(client):
    response = client.get("/api/programs/MG")
    payload = response.get_json()
    assert response.status_code == 200
    assert payload["code"] == "MG"
    assert payload["diet"].startswith("B: 4 Eggs")


def test_program_detail_endpoint_returns_404_for_unknown_program(client):
    response = client.get("/api/programs/xyz")
    assert response.status_code == 404
    assert "not found" in response.get_json()["error"].lower()


def test_calories_endpoint_returns_correct_estimate(client):
    response = client.post("/api/calories", json={"program_code": "FL", "weight_kg": 70})
    payload = response.get_json()
    assert response.status_code == 200
    assert payload["estimated_calories"] == 70 * 22
    assert payload["program_code"] == "FL"


def test_calories_endpoint_missing_fields_returns_400(client):
    response = client.post("/api/calories", json={"program_code": "FL"})
    assert response.status_code == 400


def test_calories_endpoint_unknown_program_returns_404(client):
    response = client.post("/api/calories", json={"program_code": "XX", "weight_kg": 70})
    assert response.status_code == 404


# ── v2.0.1: SQLite client management ─────────────────────────────────────────

@pytest.fixture
def tmp_db():
    """Provide a fresh temporary SQLite database for each test."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    init_db(path)
    # Point the module-level _DB_PATH to this temp file
    import src.Aceestver as ace
    original = ace._DB_PATH
    ace._DB_PATH = path
    yield path
    ace._DB_PATH = original
    try:
        os.unlink(path)
    except OSError:
        pass  # Windows may keep the file locked briefly after SQLite closes


def test_add_client_returns_201(client):
    response = client.post("/api/clients", json={
        "name": "Ravi", "age": 28, "weight_kg": 75, "program_code": "FL", "adherence": 80
    })
    assert response.status_code == 201
    payload = response.get_json()
    assert payload["name"] == "Ravi"
    assert payload["program_code"] == "FL"
    assert payload["adherence"] == 80


def test_add_client_missing_fields_returns_400(client):
    response = client.post("/api/clients", json={"name": "Ravi"})
    assert response.status_code == 400


def test_add_client_unknown_program_returns_404(client):
    response = client.post("/api/clients", json={
        "name": "Ravi", "age": 28, "weight_kg": 75, "program_code": "XX", "adherence": 50
    })
    assert response.status_code == 404


def test_list_clients_returns_all(client):
    client.post("/api/clients", json={"name": "A", "age": 20, "weight_kg": 60, "program_code": "BG", "adherence": 70})
    client.post("/api/clients", json={"name": "B", "age": 25, "weight_kg": 80, "program_code": "MG", "adherence": 90})
    response = client.get("/api/clients")
    payload = response.get_json()
    assert response.status_code == 200
    assert payload["total"] == 2
    assert payload["clients"][0]["name"] == "A"


def test_export_csv_returns_csv_file(client):
    client.post("/api/clients", json={"name": "Priya", "age": 30, "weight_kg": 65, "program_code": "FL", "adherence": 75})
    response = client.get("/api/clients/export.csv")
    assert response.status_code == 200
    assert "text/csv" in response.content_type
    assert b"Priya" in response.data


def test_chart_returns_png(client):
    client.post("/api/clients", json={"name": "Karan", "age": 22, "weight_kg": 70, "program_code": "MG", "adherence": 85})
    response = client.get("/api/chart")
    assert response.status_code == 200
    assert response.content_type == "image/png"


def test_chart_with_no_clients_returns_404(client):
    response = client.get("/api/chart")
    assert response.status_code == 404


# ── v2.1.2: Progress / session tracking ──────────────────────────────────────

def test_log_progress_returns_201(client):
    response = client.post("/api/progress", json={
        "client_name": "Ravi", "adherence": 85, "week": "Week 01 - 2025"
    })
    assert response.status_code == 201
    payload = response.get_json()
    assert payload["client_name"] == "Ravi"
    assert payload["adherence"] == 85
    assert payload["week"] == "Week 01 - 2025"


def test_log_progress_missing_fields_returns_400(client):
    response = client.post("/api/progress", json={"client_name": "Ravi"})
    assert response.status_code == 400


def test_get_progress_returns_history(client):
    client.post("/api/progress", json={"client_name": "Priya", "adherence": 70, "week": "Week 01 - 2025"})
    client.post("/api/progress", json={"client_name": "Priya", "adherence": 90, "week": "Week 02 - 2025"})
    response = client.get("/api/progress/Priya")
    payload = response.get_json()
    assert response.status_code == 200
    assert payload["total"] == 2
    assert payload["sessions"][0]["adherence"] == 70
    assert payload["sessions"][1]["adherence"] == 90


def test_get_progress_unknown_client_returns_empty(client):
    response = client.get("/api/progress/Unknown")
    payload = response.get_json()
    assert response.status_code == 200
    assert payload["total"] == 0
    assert payload["sessions"] == []
