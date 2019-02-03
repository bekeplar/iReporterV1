import pytest

from api.app import create_app
from database.db import DatabaseConnection

db = DatabaseConnection()
db.cursor.execute(open("database/schema.sql", "r").read())
db.cursor.execute(open("database/empty_tables.sql", "r").read())
db.cursor.execute(open("database/test_data.sql", "r").read())


@pytest.fixture(scope="session")
def client():
    """Tells Flask that app is in test mode
    """

    app = create_app()

    app.config.from_object("instance.config.TestingConfig")

    client = app.test_client()

    context = app.app_context()
    context.push()

    yield client
    context.pop()
