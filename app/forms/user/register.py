from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    label = "Name"
    name = StringField(label, validators=[DataRequired()], render_kw={
        "required": True,
        "type": "name",
        "placeholder": label
    })

    label = "login"
    nick = StringField(label, validators=[DataRequired()], render_kw={
        "required": True,
        "type": "login",
        "placeholder": label
    })

    label = "Password"
    password = PasswordField(label, validators=[DataRequired()], render_kw={
        "required": True,
        "type": "password",
        "placeholder": label
    })

    label = "Repeat password"
    password_again = PasswordField(label, validators=[DataRequired()], render_kw={
        "required": True,
        "type": "password",
        "placeholder": label
    })

    submit = SubmitField("OK", render_kw={
        "class": "btn btn-primary",
        "type": "submit"
    })

    def clear_errors(self):
        for item in self.items:
            item.errors = []

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        default = "form-control"
        self.items = [self.nick, self.name, self.password, self.password_again]
        self.nick.render_kw["class"] = default
        self.name.render_kw["class"] = default
        self.password.render_kw["class"] = default
        self.password_again.render_kw["class"] = default
