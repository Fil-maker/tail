from api import db
from api.models.employer import users_to_employers
from api.models.iso8601_serializer_mixin import ISO8601SerializerMixin


class Reply(db.Model, ISO8601SerializerMixin):
    __tablename__ = "replies"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    vacancy_id = db.Column(db.Integer(), db.ForeignKey("vacancies.id"))
    resume_link = db.Column(db.String(), nullable=False)
    cv_link = db.Column(db.String(), nullable=False)
    status = db.Column(db.String(), nullable=True, default=None)

    user = db.relationship("User", foreign_keys=[user_id], backref="replies")
    vacancy = db.relationship("Vacancy", foreign_keys=[vacancy_id], backref="replies")

    def to_dict(self, *args, **kwargs):
        if "only" in kwargs:
            return super(Reply, self).to_dict(*args, **kwargs)
        return super(Reply, self).to_dict(*args, **kwargs, only=["id", "resume_link", "cv_link"])
