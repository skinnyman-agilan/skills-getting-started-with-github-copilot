from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    email = "remove-me@mergington.edu"

    signup_response = client.post(
        f"/activities/Chess Club/signup?email={email}"
    )
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        f"/activities/Chess Club/unregister?email={email}"
    )
    assert unregister_response.status_code == 200

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    assert email not in activities_response.json()["Chess Club"]["participants"]


def test_unregister_participant_returns_404_for_unknown_email():
    response = client.delete(
        "/activities/Chess Club/unregister?email=does-not-exist@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
