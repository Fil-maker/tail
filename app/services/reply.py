import os
import requests
from flask_wtf import FlaskForm
from flask import request
from werkzeug.utils import secure_filename
from pathlib import Path

api_url = f"http://{os.environ.get('API_HOST')}:{os.environ.get('API_PORT')}/api/replies"
ALLOWED_EXTENSIONS = ['docx', 'doc', 'txt', 'pdf', 'md']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def is_file_for_download(filename, files):
    if filename not in files:
        return False
    file = files.get(filename)
    if file.filename == '':
        return False
    return file and allowed_file(file.filename)


def create_filename(filename, files, user_id, vacancy_id):
    file = files.get(filename)
    filename_n = secure_filename(file.filename)
    if filename_n.find('.') == -1:
        filename_n = filename + '.' + secure_filename(file.filename)
    full_filename = os.path.join(os.environ.get("UPLOAD_FOLDER") + f'/files/vac{vacancy_id}/user{user_id}/{filename}',
                                 filename_n)
    return full_filename


def save_file(filename, files, path, user_id, vacancy_id):
    file = files.get(filename)
    os.makedirs(os.environ.get("UPLOAD_FOLDER") + f'/files/vac{vacancy_id}/user{user_id}/{filename}', exist_ok=True)
    file.save(path)


def apply_vacancy_from_form(user_id, vacancy_id, form: FlaskForm):
    if form.validate_on_submit():
        resume_flag = is_file_for_download("resume_link", request.files)
        cv_flag = is_file_for_download("cv_link", request.files)
        if not resume_flag:
            form.resume_link.render_kw["class"] = "form-control is-invalid"
            form.resume_link.errors.append("Плохой формат файла")
            return {"success": False}
        if not cv_flag:
            form.cv_link.render_kw["class"] = "form-control is-invalid"
            form.cv_link.errors.append("Плохой формат файла")
            return {"success": False}
        resume_path = create_filename("resume_link", request.files, user_id, vacancy_id)
        cv_path = create_filename("cv_link", request.files, user_id, vacancy_id)
        data = apply_for_vacancy(user_id, vacancy_id, resume_path, cv_path)
        if data.get("success", None):
            save_file("resume_link", request.files, resume_path, user_id, vacancy_id)
            save_file("cv_link", request.files, cv_path, user_id, vacancy_id)
            return data
        form.submit.render_kw["class"] = "form-control is-invalid"
        form.submit.errors.append(data["message"].replace("'", ""))
    return {"success": False}


def apply_for_vacancy(user_id, vacancy_id, resume_link, cv_link):
    response = requests.post(api_url, {
        "user_id": user_id,
        "vacancy_id": vacancy_id,
        "resume_link": resume_link,
        "cv_link": cv_link
    })
    data = response.json()
    return data


def delete_reply(vacancy_id):
    response = requests.delete(f"{api_url}/{vacancy_id}")
    data = response.json()
    return data


def get_replies_by_vacancy_id(vacancy_id=None):
    response = requests.get(f"{api_url}", {"vacancy_id": vacancy_id})
    data = response.json()
    if data["success"]:
        return data["replies"]
    return None


def apply_reply(reply_id):
    response = requests.post(f"{api_url}/{reply_id}/apply")
    data = response.json()
    return data
