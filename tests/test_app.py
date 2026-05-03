import pytest
from fastapi.testclient import TestClient
from app import app, activities

# Initial activities data for resetting
initial_activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice basketball skills and compete in school games",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": []
    },
    "Soccer Club": {
        "description": "Learn soccer techniques and play friendly matches",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 22,
        "participants": []
    },
    "Art Club": {
        "description": "Express creativity through painting, drawing, and other art forms",
        "schedule": "Wednesdays, 3:00 PM - 4:30 PM",
        "max_participants": 18,
        "participants": []
    },
    "Drama Club": {
        "description": "Practice acting, stage production, and theatrical performances",
        "schedule": "Tuesdays and Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": []
    },
    "Debate Club": {
        "description": "Develop critical thinking and public speaking through debates",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": []
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Mondays, 3:00 PM - 4:30 PM",
        "max_participants": 14,
        "participants": []
    }
}

@pytest.fixture
def client():
    # Arrange: Reset activities to initial state
    activities.clear()
    activities.update(initial_activities)
    return TestClient(app)

def test_root_redirect(client):
    # Act
    response = client.get("/")
    # Assert
    assert response.status_code == 200
    assert "html" in response.text.lower()

def test_get_activities(client):
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"

def test_signup_success(client):
    # Arrange
    activity = "Basketball Team"
    email = "newstudent@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" == response.json()["message"]
    assert email in activities[activity]["participants"]

def test_signup_activity_not_found(client):
    # Arrange
    activity = "Nonexistent Activity"
    email = "test@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_signup_already_signed_up(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # Already in participants
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 400
    assert "Student already signed up for this activity" == response.json()["detail"]

def test_signup_activity_full(client):
    # Arrange
    activity = "Chess Club"
    # Fill the activity (max 12, already 2, add 10 more)
    for i in range(10):
        client.post(f"/activities/{activity}/signup", params={"email": f"user{i}@mergington.edu"})
    # Now try to add one more
    email = "last@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 400
    assert "Activity is full" == response.json()["detail"]

def test_remove_participant_success(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" == response.json()["message"]
    assert email not in activities[activity]["participants"]

def test_remove_participant_not_found(client):
    # Arrange
    activity = "Chess Club"
    email = "nonexistent@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert "Participant not found" == response.json()["detail"]

def test_remove_activity_not_found(client):
    # Arrange
    activity = "Nonexistent Activity"
    email = "test@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert "Activity not found" == response.json()["detail"]