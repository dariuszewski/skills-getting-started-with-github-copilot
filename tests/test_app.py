from urllib.parse import quote

from src import app as app_module


def activity_path(activity_name: str) -> str:
    return quote(activity_name, safe="")


def test_root_redirects_to_static_index(client):
    # Arrange
    path = "/"

    # Act
    response = client.get(path, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_map(client):
    # Arrange
    path = "/activities"

    # Act
    response = client.get(path)

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert "Chess Club" in payload
    assert "participants" in payload["Chess Club"]


def test_signup_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new-student@mergington.edu"
    path = f"/activities/{activity_path(activity_name)}/signup?email={quote(email)}"

    # Act
    response = client.post(path)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    path = f"/activities/{activity_path(activity_name)}/signup?email={quote(email)}"

    # Act
    response = client.post(path)

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_rejects_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "new-student@mergington.edu"
    path = f"/activities/{activity_path(activity_name)}/signup?email={quote(email)}"

    # Act
    response = client.post(path)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_removes_existing_participant(client):
    # Arrange
    activity_name = "Gym Class"
    email = "john@mergington.edu"
    path = f"/activities/{activity_path(activity_name)}/participants?email={quote(email)}"

    # Act
    response = client.delete(path)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_rejects_non_enrolled_participant(client):
    # Arrange
    activity_name = "Gym Class"
    email = "not-enrolled@mergington.edu"
    path = f"/activities/{activity_path(activity_name)}/participants?email={quote(email)}"

    # Act
    response = client.delete(path)

    # Assert
    assert response.status_code == 404
    assert "not signed up" in response.json()["detail"]


def test_unregister_rejects_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"
    path = f"/activities/{activity_path(activity_name)}/participants?email={quote(email)}"

    # Act
    response = client.delete(path)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
