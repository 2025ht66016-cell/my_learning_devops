import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from src.Aceestver import get_program_by_code, get_programs_summary
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



def test_program_lookup_is_case_insensitive():
    program = get_program_by_code("fl")
    assert program is not None
    assert program["name"] == "Fat Loss"


def test_program_summary_exposes_three_profiles():
    summaries = get_programs_summary()
    assert len(summaries) == 3
    assert {program["code"] for program in summaries} == {"FL", "MG", "BG"}


def test_unknown_program_code_returns_none():
    assert get_program_by_code("XX") is None


def test_health_endpoint_returns_ok_status():
    client = create_app().test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"service": "aceest-fitness", "status": "ok"}


def test_program_list_endpoint_returns_expected_payload():
    client = create_app().test_client()
    response = client.get("/api/programs")
    payload = response.get_json()

    assert response.status_code == 200
    assert len(payload["programs"]) == 3


def test_program_detail_endpoint_returns_program_data():
    client = create_app().test_client()
    response = client.get("/api/programs/MG")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["code"] == "MG"
    assert payload["diet"].startswith("B: 4 Eggs")


def test_program_detail_endpoint_returns_404_for_unknown_program():
    client = create_app().test_client()
    response = client.get("/api/programs/xyz")

    assert response.status_code == 404
    assert "not found" in response.get_json()["error"].lower()