from flask import Blueprint, jsonify, request

from api.helpers.auth_token import (
    token_required,
    non_admin,
    get_current_identity,
)

create_incident_bp = Blueprint("new_incident", __name__, url_prefix="/api/v3")
from api.models.incident import Incident
from api.helpers.validation import validate_new_incident

incident_obj = Incident()


@create_incident_bp.route("/incidents", methods=["POST"])
@token_required
@non_admin
def new_red_flag():
    if not request.data:
        return (
            jsonify({"error": "Please provide incident Data", "status": 400}),
            400,
        )
    data = request.get_json(force=True)

    new_incident_data = {
        "title": data.get("title"),
        "location": data.get("location"),
        "comment": data.get("comment"),
        "images": data.get("Images"),
        "videos": data.get("Videos"),
        "inc_type": data.get("type"),
    }

    not_valid = validate_new_incident(**new_incident_data)
    response = None
    incident_type = new_incident_data.get("inc_type")
    if not_valid:
        response = not_valid
    else:
        new_incident_data["user_id"] = get_current_identity()

        new_db_incident_details = incident_obj.insert_incident(
            **new_incident_data
        )

        response = (
            jsonify(
                {
                    "status": 201,
                    "data": [
                        {
                            incident_type: new_db_incident_details,
                            "success": "Created " + incident_type + " record",
                        }
                    ],
                }
            ),
            201,
        )

    return response
