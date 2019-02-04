from flask import Blueprint, jsonify, request

from api.helpers.auth_token import (
    non_admin,
    get_current_identity,
    token_required,
    admin_required,
)
from api.helpers.responses import wrong_status
from api.helpers.validation import (
    request_data_required,
    is_valid_uuid,
    validate_edit_location,
    is_valid_status,
    validate_sentence,
    parse_incident_type,
)
from api.models.incident import Incident

incident_obj = Incident()
edit_bp = Blueprint("edit_bp", __name__, url_prefix="/api/v1")
admin_bp = Blueprint("admin", __name__, url_prefix="/api/v1")


@edit_bp.route("/<incidents>/<incident_id>/location", methods=["PATCH"])
@token_required
@non_admin
@parse_incident_type
@is_valid_uuid
@request_data_required
def edit_incident_location(incidents, incident_id):
    data = request.get_json(force=True)
    is_invalid_location = validate_edit_location(data.get("location"))
    inc_type = incidents[:-1]

    results = incident_obj.get_incident_by_id_and_type(
        inc_id=incident_id, inc_type=inc_type
    )
    response = None

    if not results:
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
    elif is_invalid_location:
        response = (
            jsonify({"error": is_invalid_location, "status": 400}),
            400,
        )

    elif (
            results["created_by"] == get_current_identity()
            and results["status"].lower() == "draft"
    ):
        location = data.get("location")

        inc_id = incident_id
        updated_record = incident_obj.update_incident_location(
            inc_id=inc_id, location=location
        )

        response = (
            jsonify(
                {
                    "status": 200,
                    "data": [
                        {
                            "id": updated_record["id"],
                            "location": updated_record["location"],
                            "success": "Updated "
                                       + inc_type
                                       + " record’s location",
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
                    "error": "You are not allowed to modify this resource",
                }
            ),
            403,
        )
    return response


@edit_bp.route("/<incidents>/<incident_id>/comment", methods=["PATCH"])
@token_required
@non_admin
@parse_incident_type
@is_valid_uuid
@request_data_required
def edit_red_flag_comment(incidents, incident_id):
    inc_type = incidents[:-1]

    data = request.get_json(force=True)
    comment = data.get("comment")
    is_invalid = validate_sentence(comment, min_len=10)
    incident_type = inc_type

    incident_results = incident_obj.get_incident_by_id_and_type(
        inc_type=incident_type, inc_id=incident_id
    )

    response = None
    if not incident_results:
        response = (
            jsonify(
                {
                    "status": 404,
                    "error": incident_type
                             + " record with specified id does not exist",
                }
            ),
            404,
        )
    elif is_invalid:
        response = (jsonify({"error": is_invalid, "status": 400}), 400)

    elif not incident_results["created_by"] == get_current_identity():
        response = (
            jsonify(
                {
                    "status": 401,
                    "error": "You can only edit comments created by you",
                }
            ),
            401,
        )
    elif not incident_results["status"].lower() == "draft":
        response = (
            jsonify(
                {
                    "status": 403,
                    "error": (
                        "You cannot edit a record which is"
                        f" {incident_results['status']}"
                    ),
                }
            ),
            403,
        )
    else:
        comment = data.get("comment")
        updated_record = incident_obj.update_incident_comment(
            inc_id=incident_id, inc_type=incident_type, comment=comment
        )
        response = (
            jsonify(
                {
                    "status": 200,
                    "data": [
                        {
                            "id": updated_record["id"],
                            "comment": updated_record["comment"],
                            "success": "Updated "
                                       + incident_type
                                       + " record’s comment",
                        }
                    ],
                }
            ),
            200,
        )

    return response


@admin_bp.route("/<incidents>/<incident_id>/status", methods=["PATCH"])
@token_required
@admin_required
@parse_incident_type
@is_valid_uuid
@request_data_required
def edit_incident_status(incidents, incident_id):
    inc_type = incidents[:-1]
    status = request.get_json(force=True).get("status")

    incident_type = inc_type

    incident_id = incident_id
    incident_results = incident_obj.get_incident_by_id_and_type(
        inc_type=incident_type, inc_id=incident_id
    )

    response = None
    if not incident_results:
        response = (
            jsonify(
                {
                    "status": 404,
                    "error": incident_type
                             + " record with specified id does not exist",
                }
            ),
            404,
        )
    elif not is_valid_status(status):
        response = jsonify({"status": 400, "error": wrong_status}), 400

    else:

        updated_record = incident_obj.update_incident_status(
            inc_id=incident_id, inc_type=incident_type, status=status
        )

        response = (
            jsonify(
                {
                    "status": 200,
                    "data": [
                        {
                            "id": updated_record["id"],
                            "status": updated_record["status"],
                            "success": "Updated "
                                       + incident_type
                                       + " record’s status",
                        }
                    ],
                }
            ),
            200,
        )

    return response
