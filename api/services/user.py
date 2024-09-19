import re
from werkzeug.security import generate_password_hash

from api import db, User

from api.services.auth import get_token


def get_user(user_id=None, to_dict=True):
    if user_id is not None:
        user = db.session.query(User).get(user_id)
        if user is None:
            return None
        return user.to_dict() if to_dict else user
    return [item.to_dict() if to_dict else item for item in db.session.query(User).all()]


def create_user(username, email, password):
    if db.session.query(User).filter(User.email == email).first() is not None:
        raise KeyError(f"Почта  {email} уже зарегестрирована")
    pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.match(pat, email):
        raise SyntaxError(f"Адрес почты: {email} неправильный")
    user = User()
    user.email = email
    user.name = username

    user.password = generate_password_hash(password)
    db.session.add(user)
    db.session.commit()
    token = get_token(user.id)
    expires = user.token_expiration
    return user, token, expires
