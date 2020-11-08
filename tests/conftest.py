import pytest
from boilerplateapp import app_factory


@pytest.fixture
def app():
    return app_factory()
