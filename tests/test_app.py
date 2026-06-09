from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    email = "remove-me@mergington.edu"

    # Act
    signup_response = client.post(f"/activities/Chess Club/signup?email={email}")
    unregister_response = client.delete(
        f"/activities/Chess Club/unregister?email={email}"
    )
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert activities_response.status_code == 200
    assert email not in activities_response.json()["Chess Club"]["participants"]


def test_unregister_participant_returns_404_for_unknown_email():
    # Arrange
    email = "does-not-exist@mergington.edu"

    # Act
    response = client.delete(f"/activities/Chess Club/unregister?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
