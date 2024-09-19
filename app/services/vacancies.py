import os
import requests
from flask_wtf import FlaskForm

api_url = f"http://{os.environ.get('API_HOST')}:{os.environ.get('API_PORT')}/api/vacancies"


def register_vacancy_from_form(form: FlaskForm) -> bool:
    if form.validate_on_submit():
        data = register_vacancy(form.name.data, form.description.data)
        if data["success"]:
            return True
    return False


def register_vacancy(name, description):
    response = requests.post(api_url, {
        "name": name,
        "description": description
    })
    data = response.json()
    return data


def get_vacancy(vacancy_id=None):
    if vacancy_id is not None:
        response = requests.get(f"{api_url}/{vacancy_id}")
        data = response.json()
        if data["success"]:
            return data["employer"]
    else:
        response = requests.get(api_url)
        data = response.json()
        if data["success"]:
            return data["employer"]
    return None
