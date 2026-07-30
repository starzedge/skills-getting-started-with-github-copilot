from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_existing_participant():
    email = "newstudent@mergington.edu"
    activity_name = "Chess Club"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    remove_response = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert remove_response.status_code == 200
    assert remove_response.json()["message"] == f"Removed {email} from {activity_name}"

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    participants = activities_response.json()[activity_name]["participants"]
    assert email not in participants


def test_unregister_participant_returns_404_for_unknown_participant():
    response = client.delete("/activities/Chess Club/participants/ghost@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
