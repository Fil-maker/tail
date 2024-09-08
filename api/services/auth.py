import datetime
import secrets

from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from sqlalchemy import or_
from werkzeug.security import check_password_hash

from api import db
from api.models import User

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    user = db.session.query(User).filter(or_(User.email == username, User.username == username)).first()
    if user is None:
        return False
    if check_password_hash(user.password, password):
        g.current_user = user
        return True
    return False


@token_auth.verify_token
def verify_token(token):
    user = db.session.query(User).filter(User.token == token).first()
    if user is None or user.token_expiration < datetime.datetime.now():
        return False
    g.current_user = user
    return True


def get_token(user_id, expires_in=3600 * 24):
    user = db.session.query(User).get(user_id)
    if user is None:
        return None
    now = datetime.datetime.now()
    if user.token and user.token_expiration > now + datetime.timedelta(seconds=60):
        # Если токен действительный, возвращаем его
        return user.token
    # Иначе, генерируем новый и устанавливаем срок истечения (по умолчанию через 24 часа)
    user.token = secrets.token_urlsafe(32)
    user.token_expiration = now + datetime.timedelta(seconds=expires_in)
    db.session.commit()
    return user.token


def revoke_token(user_id):
    # Отзыв токена (Время истечения изменяется на текущее - 1 секунда)
    user = db.session.query(User).get(user_id)
    if user is None:
        return False
    user.token_expiration = datetime.datetime.now() - datetime.timedelta(seconds=1)
    db.session.commit()
    return True


@basic_auth.error_handler
def basic_auth_error():
    return jsonify({'success': False}), 401


@token_auth.error_handler
def token_auth_error():
    return jsonify({'success': False}), 401
