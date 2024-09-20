from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class VacancyApplyForm(FlaskForm):
    resume_link = FileField('Резюме', validators=[DataRequired()], render_kw={
        "class": "form-photo",
        "required": True,
    })
    cv_link = FileField('Сопроводительное письмо', validators=[DataRequired()], render_kw={
        "class": "form-photo",
        "required": True,
    })

    submit = SubmitField("OK", render_kw={
        "class": "btn btn-primary",
        "type": "submit"
    })

    def clear_errors(self):
        for item in self.items:
            item.errors = []

    def __init__(self, *args, **kwargs):
        super(VacancyApplyForm, self).__init__(*args, **kwargs)
        default = "form-control"
        self.items = [self.resume_link, self.cv_link]
        self.resume_link.render_kw["class"] = default
        self.cv_link.render_kw["class"] = default
