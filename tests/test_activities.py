from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# GET /activities
# ---------------------------------------------------------------------------

def test_get_activities_returns_all(client: TestClient):
    # Arrange — initial db is populated by conftest reset_activities fixture

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_get_activities_returns_expected_structure(client: TestClient):
    # Arrange — any existing activity is sufficient

    # Act
    response = client.get("/activities")

    # Assert
    activity = next(iter(response.json().values()))
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity


# ---------------------------------------------------------------------------
# POST /activities/{activity_name}/signup
# ---------------------------------------------------------------------------

def test_signup_success(client: TestClient):
    # Arrange
    email = "new.student@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    participants = client.get("/activities").json()["Chess Club"]["participants"]
    assert email in participants


def test_signup_duplicate_returns_400(client: TestClient):
    # Arrange — michael is already in Chess Club from the initial data
    email = "michael@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 400


def test_signup_unknown_activity_returns_404(client: TestClient):
    # Arrange
    email = "student@mergington.edu"

    # Act
    response = client.post("/activities/Unknown Activity/signup", params={"email": email})

    # Assert
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# DELETE /activities/{activity_name}/signup
# ---------------------------------------------------------------------------

def test_unregister_success(client: TestClient):
    # Arrange — michael is already in Chess Club
    email = "michael@mergington.edu"

    # Act
    response = client.delete("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    participants = client.get("/activities").json()["Chess Club"]["participants"]
    assert email not in participants


def test_unregister_not_signed_up_returns_400(client: TestClient):
    # Arrange — this email is not in Chess Club
    email = "nobody@mergington.edu"

    # Act
    response = client.delete("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 400


def test_unregister_unknown_activity_returns_404(client: TestClient):
    # Arrange
    email = "student@mergington.edu"

    # Act
    response = client.delete("/activities/Unknown Activity/signup", params={"email": email})

    # Assert
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# GET / (redirect)
# ---------------------------------------------------------------------------

def test_root_redirects_to_static(client: TestClient):
    # Arrange — no setup needed

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (301, 302, 307, 308)
    assert response.headers["location"].endswith("/static/index.html")
