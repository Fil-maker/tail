import os
import requests
from flask import session, g
from flask_wtf import FlaskForm
from requests.auth import AuthBase
from werkzeug.utils import redirect

api_url = f"http://{os.environ.get('API_HOST')}:{os.environ.get('API_PORT')}/api/users"


class HTTPTokenAuth(AuthBase):
    def __init__(self, token=None):
        if token is None:
            token = session.get("token", "")
        self.token = token

    def __eq__(self, other):
        return self.token == getattr(other, "token", None)

    def __ne__(self, other):
        return not self == other

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r


def redirect_if_authorized(func):
    def new_func(*args, **kwargs):
        token = session.get("token", None)
        if token:
            return redirect("/")
        return func(*args, **kwargs)

    new_func.__name__ = func.__name__
    return new_func


def redirect_if_unauthorized(func):
    def new_func(*args, **kwargs):
        token = session.get("token", None)
        if token is None:
            return redirect("/login")
        return func(*args, **kwargs)

    new_func.__name__ = func.__name__
    return new_func


def login_from_form(form: FlaskForm) -> bool:
    if form.validate_on_submit():
        data = login_user(form.login.data, form.password.data)
        if data["success"]:
            return True
        form.login.render_kw["class"] = "form-control is-invalid"
        form.password.render_kw["class"] = "form-control is-invalid"
        form.password.errors.append("Неправильный логин или пароль")
    return False


def logout():
    response = requests.post(f"{api_url}/logout", auth=HTTPTokenAuth())
    if response.json()["success"]:
        session.pop("token", None)
        g.current_user = None
        return True
    return False


def login_user(login, password):
    response = requests.post(f"{api_url}/login", auth=(login, password))
    data = response.json()
    if data["success"]:
        session["token"] = data["authToken"]["token"]
        g.current_user = data["user"]
    return data


def register_from_form(form: FlaskForm) -> bool:
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            form.password.render_kw["class"] = "form-control is-invalid"
            form.password_again.render_kw["class"] = "form-control is-invalid"
            form.password_again.errors.append("Пароли не совпадают")
            return False
        if int(os.environ.get("CHECK_PASSWORD_STRENGTH", 1)) and not is_password_secure(form.password.data):
            form.password.render_kw["class"] = "form-control is-invalid"
            form.password.errors.append("Ненадёжный пароль")
            return False
        data = register_user(form.email.data, form.name.data, form.password.data)
        if data["success"]:
            return True
        message = data['message'].replace("'", "")
        form.email.render_kw["class"] = "form-control is-invalid"
        form.email.errors.append(f"{message}")
    return False


def register_user(email, name, password):
    response = requests.post(api_url, {
        "email": email,
        "username": name,
        "password": password,
    })
    data = response.json()
    if data.get("success") is not None:
        pass
        # session["token"] = data["authToken"]["token"]
        # g.current_user = data["user"]
    return data


def get_user(user_id=None):
    if user_id is not None:
        response = requests.get(f"{api_url}/{user_id}")
        data = response.json()
        if data["success"]:
            return data["user"]
    else:
        response = requests.get(api_url)
        data = response.json()
        if data["success"]:
            return data["users"]
    return None


def get_myself():
    response = requests.get(f"{api_url}/get-myself", auth=HTTPTokenAuth())
    data = response.json()
    if data["success"]:
        return data["user"]
    return None


def is_password_secure(password: str) -> bool:
    return not (len(password) < 8 or
                password.isdigit() or
                password.isalpha() or
                password.islower() or
                password.isupper())


def get_users_by_name(name):
    response = requests.get(f"{api_url}/get_by_name/{name}")
    data = response.json()
    return data
