from flask import Blueprint, jsonify, request

from api.helpers.auth_token import (
    token_required,
    non_admin,
    admin_required,
    get_current_identity,
)
from api.helpers.validation import (
    # is_valid_uuid, 
    #parse_incident_type,
    request_data_required
    )
from api.controllers.incident import IncidentController
incident_controller = IncidentController()


create_incident_bp = Blueprint("new_redflag", __name__, url_prefix="/api/v1")
create_incident_bp = Blueprint("new_intervention", __name__, url_prefix="/api/v1")
get_inc_bp = Blueprint("get_incidents", __name__, url_prefix="/api/v1")
del_inc_bp = Blueprint("del_inc_bp", __name__, url_prefix="/api/v1")
edit_bp = Blueprint("edit_bp", __name__, url_prefix="/api/v1")
admin_bp = Blueprint("admin", __name__, url_prefix="/api/v1")

@create_incident_bp.route("/redflags", methods=["POST"])
@token_required
@non_admin
def new_redflag():
    data = request.get_json(force=True)
    return incident_controller.new_incident(data, 'redflag')


@get_inc_bp.route("/redflags", methods=["GET"])
@token_required
def get_all():
    return incident_controller.get_incidents('redflag')

@create_incident_bp.route("/interventions", methods=["POST"])
@token_required
@non_admin
def create_new_intervention():
    data = request.get_json(force=True)
    return incident_controller.new_incident(data, 'intervention')

@get_inc_bp.route("/interventions", methods=["GET"])
@token_required
def get_all_interventions():
    return incident_controller.get_incidents('interventions')


@get_inc_bp.route("/<redflags>/<redflag_id>", methods=["GET"])
@token_required
# @parse_incident_type
# @is_valid_uuid
def get_one_redflag(redflag_id):
    return incident_controller.get_a_specific_incident(redflag_id, 'redflag')

@del_inc_bp.route("/redflags/<redflag_id>", methods=["DELETE"])
@token_required
@non_admin
# @parse_incident_type
# @is_valid_uuid
def delete_one(redflag_id):
    return incident_controller.delete_record(redflag_id, 'redflag')

@edit_bp.route("/redflags/<redflag_id>/location", methods=["PATCH"])
@token_required
@non_admin
# @parse_incident_type
# @is_valid_uuid
@request_data_required
def update_location(redflag_id):
    return incident_controller.edit_incident_location(redflag_id, 'redflag')

@edit_bp.route("/redflags/<redflag_id>/comment", methods=["PATCH"])
@token_required
@non_admin
# @parse_incident_type
# @is_valid_uuid
@request_data_required
def update_comment(redflag_id):
    return incident_controller.edit_red_flag_comment(redflag_id, 'redflag')


@admin_bp.route("/redflags/<redflag_id>/status", methods=["PATCH"])
@token_required
@admin_required
# @parse_incident_type
# @is_valid_uuid
@request_data_required
def change_status(redflag_id):
    return incident_controller.edit_incident_status(redflag_id, 'redflag')