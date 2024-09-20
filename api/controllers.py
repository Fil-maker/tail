import datetime
import json
import os
from flask import g, jsonify, request
from flask_restful.reqparse import RequestParser

from api import app, db
from api.services.auth import basic_auth, get_token, token_auth, revoke_token
from api.services.employer import subscribe_user_to_employer, unsubscribe_user_from_employer
from api.services.reply import apply_reply
from api.services.user import get_users_by_name

app_url = f"http://{os.environ.get('APP_HOST')}:{os.environ.get('APP_PORT')}"


@app.route("/api/users/login", methods=["POST"])
@basic_auth.login_required
# Путь получает в заголовках запроса логин и пароль пользователя (декоратор @basic.auth.login_required)
# и, если данные верны, возвращает токен. Чтобы защитить маршруты API с помощью токенов, необходимо
# добавить декоратор @token_auth.login_required
def log_in():
    token = get_token(g.current_user.id)
    return jsonify({"success": True, "user": g.current_user.to_dict(),
                    "authToken": {"token": token,
                                  "expires": str(g.current_user.token_expiration)}})


@app.route("/api/users/logout", methods=["POST"])
@token_auth.login_required
# Отзыв токена
def log_out():
    revoke_token(g.current_user.id)
    g.current_user = None
    return jsonify({"success": True})


@app.route("/api/users/get-myself")
@token_auth.login_required
def get_myself():
    return jsonify({"success": True, "user": g.current_user.to_dict()})


@app.route("/api/employers/<int:employer_id>/subscribe/<int:user_id>", methods=["POST"])
def subscribe_user_to_employer_controller(user_id, employer_id):
    try:
        employer = subscribe_user_to_employer(user_id, employer_id)
    except Exception as e:
        return jsonify({"success": False, "message": str(e), "error_code": 400})
    else:
        return jsonify({"success": True, "employer": employer.to_dict()})


@app.route("/api/employers/<int:employer_id>/unsubscribe/<int:user_id>", methods=["POST"])
def unsubscribe_user_from_employer_controller(user_id, employer_id):
    try:
        employer = unsubscribe_user_from_employer(user_id, employer_id)
    except Exception as e:
        return jsonify({"success": False, "message": str(e), "error_code": 400})
    else:
        return jsonify({"success": True, "employer": employer.to_dict()})


@app.route("/api/users/get_by_name/<string:name>")
def get_users_by_name_controller(name):
    try:
        users = get_users_by_name(name)
    except Exception as e:
        return jsonify({"success": False, "message": str(e), "error_code": 400})
    else:
        return jsonify({"success": True, "users": users})


@app.route("/api/replies/<int:reply_id>/apply", methods=["POST"])
def apply_reply_controller(reply_id):
    try:
        reply = apply_reply(reply_id)
    except Exception as e:
        return jsonify({"success": False, "message": str(e), "error_code": 400})
    else:
        return jsonify({"success": True, "reply": reply.to_dict()})
