from flask import jsonify, Blueprint, session, g, request
from flask_restful.reqparse import RequestParser

from app.services.employer import subscribe_user_to_employer, unsubscribe_user_from_employer, add_user_to_employer
from app.services.reply import apply_reply
from app.services.user import get_myself, get_users_by_name

ajax = Blueprint("ajax", __name__)


@ajax.before_request
def before_request():
    if session.get("token", None):
        current_user = get_myself()
        if current_user is None:
            session.pop("token", None)
            return 401
        g.current_user = current_user


@ajax.route("/employer/<int:employer_id>/subscribe/<int:user_id>", methods=["POST"])
def subscribe_user_to_employer_ajax(employer_id, user_id):
    data = subscribe_user_to_employer(user_id, employer_id)
    return jsonify(data), 200 if data["success"] else 400


@ajax.route("/employer/<int:employer_id>/unsubscribe/<int:user_id>", methods=["POST"])
def unsubscribe_user_to_employer_ajax(employer_id, user_id):
    data = unsubscribe_user_from_employer(user_id, employer_id)
    return jsonify(data), 200 if data["success"] else 400


@ajax.route("/employer/<int:employer_id>/add_user/<int:user_id>", methods=["POST"])
def add_user_to_employer_ajax(employer_id, user_id):
    data = add_user_to_employer(user_id, employer_id)
    return jsonify(data), 200 if data["success"] else 400


@ajax.route("/users/get_by_name/<string:name>", methods=["POST"])
def get_users_by_name_ajax(name):
    data = get_users_by_name(name)
    return jsonify(data), 200 if data["success"] else 400


@ajax.route("/replies/<int:reply_id>/apply", methods=["POST"])
def apply_reply_ajax(reply_id):
    data = apply_reply(reply_id)
    return jsonify(data), 200 if data["success"] else 400
