"""Contains function that creates the app"""
from flask import Flask, jsonify
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from api.views.auth import users_bp
from api.views.create_incident import create_incident_bp
from api.views.delete_incident import del_inc_bp
from api.views.edit_incident import edit_bp, admin_bp
from api.views.get_incidents import get_inc_bp
from instance.config import Config


def create_app(config=None):
    """Set up Flask application in function"""
    app = Flask(__name__)
    CORS(app)

    @app.route("/")
    @app.route("/api/v3")
    def _hello_ireporter():
        return (
            jsonify({"message": "Welcome to iReporter API V3", "status": 200}),
            200,
        )

    @app.errorhandler(400)
    def _page_not_found(e):
        return (jsonify({"error": "Bad JSON format data", "status": 400}), 400)

    @app.errorhandler(401)
    def _not_authorized(e):
        return (
            jsonify(
                {
                    "error": "You are not authorized to access this resource",
                    "status": 401,
                }
            ),
            401,
        )

    @app.errorhandler(404)
    def _page_not_found(e):
        return (
            jsonify({"error": "Endpoint for specified URL does not exist"}),
            404,
        )

    @app.errorhandler(405)
    def _method_not_allowed(e):
        return (jsonify({"error": "Method not allowed"}), 405)

    app.config.from_object(Config)
    app.register_blueprint(users_bp)
    app.register_blueprint(create_incident_bp)
    app.register_blueprint(get_inc_bp)
    app.register_blueprint(edit_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(del_inc_bp)
    SWAGGER_UI_URL = "/api/v3/docs"
    API_URL = "https://kalsmic.github.io/swagger-ui/dist/ireporter_api_v3.json"

    swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_UI_URL, API_URL)
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_UI_URL)
    return app
