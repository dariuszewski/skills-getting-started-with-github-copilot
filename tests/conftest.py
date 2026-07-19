from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities_state():
    """Reset in-memory activities so tests stay isolated."""
    original_state = deepcopy(app_module.activities)

    yield

    app_module.activities.clear()
    app_module.activities.update(deepcopy(original_state))


@pytest.fixture
def client():
    with TestClient(app_module.app) as test_client:
        yield test_client
