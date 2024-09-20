from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class VacancyRegisterForm(FlaskForm):
    label = "Название вакансии"
    name = StringField(label, validators=[DataRequired()], render_kw={
        "required": True,
        "type": "name",
        "placeholder": label
    })

    label = "Описание"
    description = TextAreaField(label, validators=[DataRequired()], render_kw={
        "required": True,
        "type": "login",
        "rows": 11,
        "cols": 90,
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
        super(VacancyRegisterForm, self).__init__(*args, **kwargs)
        default = "form-control"
        self.items = [self.name, self.description]
        self.name.render_kw["class"] = default
        self.description.render_kw["class"] = default
