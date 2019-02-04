from flask import Blueprint, jsonify

from api.helpers.auth_token import (
    token_required,
    non_admin,
    get_current_identity,
)
from api.helpers.responses import delete_not_allowed
from api.helpers.validation import (
    is_valid_uuid,
    parse_incident_type,
)
from api.models.incident import Incident

incident_obj = Incident()
del_inc_bp = Blueprint("del_inc_bp", __name__, url_prefix="/api/v1")


@del_inc_bp.route("/<incidents>/<incident_id>", methods=["DELETE"])
@token_required
@non_admin
@parse_incident_type
@is_valid_uuid
def delete_record(incidents, incident_id):
    incident_type = incidents[:-1]
    response = None

    results = incident_obj.get_incident_by_id_and_type(
        inc_type=incident_type, inc_id=incident_id
    )

    if not results:
        response = (
            jsonify(
                {
                    "status": 404,
                    "error": incident_type + " record does not exist",
                }
            ),
            404,
        )
    elif not results["created_by"] == get_current_identity():

        response = (jsonify({"status": 403, "error": delete_not_allowed}), 403)
    elif results["status"].lower() == "draft":
        delete_id = incident_obj.delete_incident_record(
            inc_id=incident_id,
            inc_type=incident_type,
            user_id=get_current_identity(),
        )

        response = (
            jsonify(
                {
                    "status": 200,
                    "data": [
                        {
                            "incident": delete_id,
                            "success": incident_type
                                       + " record has been deleted",
                        }
                    ],
                }
            ),
            200,
        )
    else:
        response = (
            jsonify(
                {
                    "status": 403,
                    "error": (
                        "You are not allowed to delete a record which is"
                        f" {results['status']}"
                    ),
                }
            ),
            403,
        )
    return response
