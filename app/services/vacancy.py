import os
import requests

from flask_wtf import FlaskForm

api_url = f"http://{os.environ.get('API_HOST')}:{os.environ.get('API_PORT')}/api/vacancies"


def register_vacancy_from_form(user_id, employer_id, form: FlaskForm):
    if form.validate_on_submit():
        data = register_vacancy(user_id, employer_id, form.name.data, form.description.data)
        if data.get("success", None):
            return data
        form.description.render_kw["class"] = "form-control is-invalid"
        form.description.errors.append(data["message"].replace("'", ""))
    return {"success": False}


def register_vacancy(user_id, employer_id, name, description):
    response = requests.post(api_url, {
        "user_id": user_id,
        "employer_id": employer_id,
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
            return data["vacancy"]
    else:
        response = requests.get(api_url)
        data = response.json()
        if data["success"]:
            return data["vacancies"]
    return None
