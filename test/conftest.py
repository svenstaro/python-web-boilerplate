import pytest
from application import app_factory


@pytest.fixture
def app():
    return app_factory()
