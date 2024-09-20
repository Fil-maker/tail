import os
import requests
from flask_wtf import FlaskForm

api_url = f"http://{os.environ.get('API_HOST')}:{os.environ.get('API_PORT')}/api/employers"


def register_employer_from_form(user_id, form: FlaskForm) -> dict:
    if form.validate_on_submit():
        data = register_employer(form.name.data, form.description.data)
        if data.get("success", None):
            data = add_user_to_employer(user_id, data["employer"]["id"])
            return data
        form.description.render_kw["class"] = "form-control is-invalid"
        form.description.errors.append(data["message"].replace("'", ""))
    return {"success": False}


def register_employer(name, description):
    response = requests.post(api_url, {
        "name": name,
        "description": description
    })
    data = response.json()
    return data


def get_employer(employer_id=None):
    if employer_id is not None:
        response = requests.get(f"{api_url}/{employer_id}")
        data = response.json()
        if data["success"]:
            return data["employer"]
    else:
        response = requests.get(api_url)
        data = response.json()
        if data["success"]:
            return data["employer"]
    return None


def add_user_to_employer(user_id, employer_id):
    response = requests.put(f"{api_url}/{employer_id}", data={"user_id": user_id})
    data = response.json()
    return data


def subscribe_user_to_employer(user_id, employer_id):
    response = requests.post(f"{api_url}/{employer_id}/subscribe/{user_id}")
    data = response.json()
    return data


def unsubscribe_user_from_employer(user_id, employer_id):
    response = requests.post(f"{api_url}/{employer_id}/unsubscribe/{user_id}")
    data = response.json()
    return data
