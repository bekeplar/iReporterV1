from flask import Flask, jsonify
from api.views.user import users_bp
from api.views.incident import (
    create_incident_bp,
    del_inc_bp,
    edit_bp, 
    admin_bp,
    get_inc_bp
    )
from instance.config import app_config


def create_app(config_name):
    """Set up Flask application in function"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    @app.route("/")
    def _home():
        return (
            jsonify({"message": "Welcome to iReporter Api V1", "status": 200}),
            200,
        )

    def _not_authorized(e):
        return (
            jsonify(
                {
                    "error":"Wrong login credentials",
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

    app.register_blueprint(users_bp)
    app.register_blueprint(create_incident_bp)
    app.register_blueprint(get_inc_bp)
    app.register_blueprint(edit_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(del_inc_bp)
   
    return app