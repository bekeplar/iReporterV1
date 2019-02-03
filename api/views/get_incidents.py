from flask import Blueprint, jsonify

from api.helpers.auth_token import token_required
from api.helpers.validation import is_valid_uuid, parse_incident_type
from api.models.incident import Incident

get_inc_bp = Blueprint("get_incidents", __name__, url_prefix="/api/v3")

incident_obj = Incident()


@get_inc_bp.route("/<path:incidents>", methods=["GET"])
@token_required
def get_all_incidents(incidents):
    results = incident_obj.get_all_incident_records(inc_type=incidents[:-1])

    return jsonify({"status": 200, "data": results}), 200


@get_inc_bp.route("/<incidents>/<incident_id>", methods=["GET"])
@token_required
@parse_incident_type
@is_valid_uuid
def get_a_red_flag(incidents, incident_id):
    inc_type = incidents[:-1]
    results = incident_obj.get_an_incident_record_(
        inc_type=inc_type, inc_id=incident_id
    )

    response = None
    if results and "error" in results:
        response = (jsonify({"status": 401, "error": results["error"]}), 401)
    elif results:
        response = jsonify({"status": 200, "data": [results]}), 200
    else:

        response = (
            jsonify(
                {
                    "status": 404,
                    "error": inc_type
                             + " record with specified id does not exist",
                }
            ),
            404,
        )

    return response
