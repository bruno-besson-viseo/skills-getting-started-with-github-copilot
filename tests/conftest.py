import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

# Snapshot of initial data taken once at import time
_initial_activities = copy.deepcopy(activities)


@pytest.fixture()
def client():
    return TestClient(app)


# Restore in-memory store to its original state before every test
@pytest.fixture(autouse=True)
def reset_activities():
    for name, data in _initial_activities.items():
        activities[name] = copy.deepcopy(data)
