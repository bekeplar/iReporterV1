"""This is the app entry point"""

from api.app import create_app
from instance.config import app_config

app = create_app("Development")
# app.config.from_object(environ.get("APP_SETTINGS"))

if __name__ == "__main__":
    app.run()
