"""This is the app entry point"""
from os import environ

from api.app import create_app

app = create_app()
app.config.from_object(environ.get("APP_SETTINGS"))

if __name__ == "__main__":
    app.run()
