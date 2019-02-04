import pytest

from api.app import create_app
from database.db import DatabaseConnection

db = DatabaseConnection('Database_url')


@pytest.fixture(scope="session")
def client():
    """Tells Flask that app is in test mode
    """

    app = create_app("Testing")

    app.config.from_object("instance.config.TestingConfig")

    client = app.test_client()

    context = app.app_context()
    context.push()

    yield client
    context.pop()
