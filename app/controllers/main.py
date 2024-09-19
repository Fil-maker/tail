from flask import render_template, g, session, request
from werkzeug.utils import redirect

from app import app
from app.forms.user.login import LoginForm

from app.services.user import login_from_form, register_from_form, logout, get_myself, \
    redirect_if_authorized, redirect_if_unauthorized


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

    # return g.current_user
    return render_template("/main_page.html", user=g.current_user)


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


@app.route("/signup")
def signup_page():
    pass
