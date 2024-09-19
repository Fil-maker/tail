import datetime
import json
import os
from flask import g, jsonify, request
from flask_restful.reqparse import RequestParser

from api import app, db
from api.services.auth import basic_auth, get_token, token_auth, revoke_token

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
