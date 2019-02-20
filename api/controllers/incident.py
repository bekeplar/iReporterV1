from flask import Blueprint, jsonify, request
from api.models.incident import Incident
from api.utilitiez.auth_token import get_current_identity
from api.utilitiez.responses import delete_not_allowed, wrong_status
from api.utilitiez.validation import (
    validate_new_incident,
    request_data_required,
    validate_edit_location,
    is_valid_status,
    validate_sentence,
)


incident_obj = Incident()

class IncidentController:
    """
    Class containing all logic connecting incident views and models.
    """

    def new_incident(self, data, ireporter):
        if not request.data:
            return (
                jsonify({"error": "Please provide some incident data", "status": 400}),
                400,
            )
        data = request.get_json()

        new_incident_data = {
            "title": data.get("title"),
            "location": data.get("location"),
            "comment": data.get("comment"),
            "created_by": data.get("user_id"),
            "inc_type": data.get("type"),
        }

        not_valid = validate_new_incident(**new_incident_data)
        response = None
        incident_type = new_incident_data.get("inc_type")
        if not_valid:
            response = not_valid
        incident_exists = incident_obj.check_incident_exists(
            new_incident_data["title"], new_incident_data["comment"]
        )
        response = None
        if incident_exists:
            response = jsonify({"error": incident_exists, "status": 409}), 409

        else:
            new_incident_data["user_id"] = get_current_identity()
            new_incident = incident_obj.create_incident(**new_incident_data)
            response = (
                jsonify(
                    {
                        "status": 201,
                        "data": [
                            {
                                incident_type: new_incident,
                                "success": f"Created {ireporter} record",
                            }
                        ],
                    }
                ),
                201,
            )
        return response
    

    def get_incidents(self, ireporter):
        results = incident_obj.get_all_records(inc_type=ireporter)

        return jsonify({"status": 200,
               "data": results, 
               "message": f"{ireporter} records found"}), 200

    def get_a_specific_incident(self, incident_id, ireporter):
        results = incident_obj.get_incident_by_id_and_type(
        inc_type=ireporter, inc_id=incident_id
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
                        "error": f"{ireporter} record with specified id does not exist"
                    }
                ),
                404,
            )

        return response

    def delete_record(self, incident_id, ireporter):
        response = None

        results = incident_obj.get_incident_by_id_and_type(
            inc_type=ireporter, inc_id=incident_id
        )

        if not results:
            response = (
                jsonify(
                    {
                        "status": 404,
                        "error": f"{ireporter} record does not exist",
                    }
                ),
                404,
            )
        elif not results["created_by"] == get_current_identity():

            response = (jsonify({"status": 403, "error": delete_not_allowed}), 403)
        elif results["status"].lower() == "draft":
            delete_id = incident_obj.delete_incident_record(
                inc_id=incident_id,
                inc_type=ireporter,
                user_id=get_current_identity(),
            )

            response = (
                jsonify(
                    {
                        "status": 200,
                        "data": [
                            {
                                "incident": delete_id,
                                "success": f"{ireporter} record has been deleted"
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

    def edit_comment_of_incident(self, incident_id, ireporter):
        inc_type = ireporter

        data = request.get_json(force=True)
        comment = data.get("comment")
        is_invalid = validate_sentence(comment, min_len=10)
        incident_type = inc_type

        incident_results = incident_obj.get_incident_by_id_and_type(
            inc_type=ireporter, inc_id=incident_id
        )

        response = None
        if not incident_results:
            response = (
                jsonify(
                    {
                        "status": 404,
                        "error": f"{ireporter} record with specified id does not exist",
                                
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
                        "error": "Only the author can update an incident record",
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
                                "success": f"Updated {incident_type} record's comment",
                            }
                        ],
                    }
                ),
                200,
            )

        return response

    def edit_incident_status(self, incident_id, ireporter):
        inc_type = ireporter[:-1]
        status = request.get_json(force=True).get("status")

        incident_type = inc_type

        incident_id = incident_id
        incident_results = incident_obj.get_incident_by_id_and_type(
            inc_type=ireporter, inc_id=incident_id
        )

        response = None
        if not incident_results:
            response = (
                jsonify(
                    {
                        "status": 404,
                        "error": f"{ireporter} record with specified id does not exist",
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
                                "success": f"Updated {incident_type} record's status",
                            }
                        ],
                    }
                ),
                200,
            )

        return response

    def edit_incident_location(self, incident_id, ireporter):
        data = request.get_json(force=True)
        is_invalid_location = validate_edit_location(data.get("location"))

        results = incident_obj.get_incident_by_id_and_type(
            inc_id=incident_id, inc_type=ireporter
        )
        response = None

        if not results:
            response = (
                jsonify(
                    {
                        "status": 404,
                        "error": f"{ireporter} record with specified id does not exist",
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
                                "success": f"Updated {ireporter} record's location",
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
                        "error": "You cannot update this resource",
                    }
                ),
                403,
            )
        return response

