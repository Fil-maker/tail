from flask import render_template, g, session, request, send_file
from werkzeug.utils import redirect

from app import app
from app.forms.employer.register import EmployerRegisterForm
from app.forms.user.login import LoginForm
from app.forms.user.register import RegisterForm
from app.forms.vacancy.apply import VacancyApplyForm
from app.forms.vacancy.register import VacancyRegisterForm
from app.services.employer import register_employer_from_form, get_employer
from app.services.reply import apply_vacancy_from_form, get_replies_by_vacancy_id

from app.services.user import login_from_form, register_from_form, logout, get_myself, \
    redirect_if_authorized, redirect_if_unauthorized
from app.services.vacancy import get_vacancy, register_vacancy_from_form


@app.before_request
def before_request():
    if session.get("token", None):
        current_user = get_myself()
        if current_user is None:
            session.pop("token", None)
            return redirect("/")
        g.current_user = current_user


@app.route("/")
@redirect_if_unauthorized
def index_page():
    vacancies = get_vacancy()
    # return g.current_user
    return render_template("/main_page.html", user=g.current_user, vacancies=vacancies)


@app.route("/login", methods=["GET", "POST"])
@redirect_if_authorized
def login_page():
    form = LoginForm()
    if login_from_form(form):
        return redirect("/")
    return render_template("/login.html", form=form)


@app.route("/logout")
def logout_page():
    logout()
    return redirect("/")


@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    form = RegisterForm()
    if request.method == "POST" and register_from_form(form):
        return redirect("/")
    return render_template("register.html", form=form)


@app.route("/new-employer", methods=["GET", "POST"])
@redirect_if_unauthorized
def register_employer_page():
    form = EmployerRegisterForm()
    if request.method == "POST":
        resp = register_employer_from_form(g.current_user["id"], form)
        if resp["success"]:
            return redirect(f"/employer/{resp['employer']['id']}")
    return render_template("register_employer.html", form=form)


@app.route("/employer/<int:employer_id>")
def employer_page(employer_id):
    employer = get_employer(employer_id)
    return render_template("employer.html", user=g.get("current_user", None), employer=employer)


@app.route("/employer/<int:employer_id>/new-vacancy", methods=["GET", "POST"])
@redirect_if_unauthorized
def register_vacancy_page(employer_id):
    employer = get_employer(employer_id)
    form = VacancyRegisterForm()
    if request.method == "POST":
        resp = register_vacancy_from_form(g.current_user["id"], employer_id, form)
        if resp["success"]:
            return redirect(f"/employer/{resp['vacancy']['employer_id']}")
    return render_template("register_vacancy.html", user=g.current_user, employer=employer, form=form)


@app.route("/employer/<int:employer_id>/reply/<int:vacancy_id>", methods=["GET", "POST"])
@redirect_if_unauthorized
def apply_for_vacancy_page(employer_id, vacancy_id):
    employer = get_employer(employer_id)
    vacancy = get_vacancy(vacancy_id)
    form = VacancyApplyForm()
    if request.method == "POST":
        resp = apply_vacancy_from_form(g.current_user["id"], vacancy_id, form)
        if resp["success"]:
            return redirect(f"/employer/{resp['reply']['employer_id']}")
    return render_template("register_reply.html", user=g.current_user, employer=employer, vacancy=vacancy, form=form)


@app.route("/employer/<int:employer_id>/check/<int:vacancy_id>", methods=["GET", "POST"])
@redirect_if_unauthorized
def check_replies_page(employer_id, vacancy_id):
    employer = get_employer(employer_id)
    vacancy = get_vacancy(vacancy_id)
    replies = get_replies_by_vacancy_id(vacancy_id)
    return render_template("check_replies.html",
                           user=g.current_user, employer=employer, vacancy=vacancy, replies=replies)


@app.route("/download/<path:path>")
def download_docs(path):
    return send_file(path, as_attachment=True)
