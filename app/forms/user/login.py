from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    label = "Электронная почта"
    login = StringField(label, validators=[DataRequired()], render_kw={
        "class": "form-control",
        "required": True,
        "type": "name",
        "placeholder": label
    })

    label = "Password"
    password = PasswordField(label, validators=[DataRequired()], render_kw={
        "class": "form-control",
        "required": True,
        "type": "password",
        "placeholder": label
    })

    submit = SubmitField("Log in", render_kw={
        "class": ""
    })

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        default = "form-control"
        self.items = [self.login, self.password]
        self.login.render_kw["class"] = default
