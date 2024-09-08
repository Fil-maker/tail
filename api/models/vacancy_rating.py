from api import db
from api.models.iso8601_serializer_mixin import ISO8601SerializerMixin


class VacancyRating(db.Model, ISO8601SerializerMixin):
    __tablename__ = "vacancy_ratings"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    vacancy_id = db.Column(db.Integer(), db.ForeignKey("vacancies.id"))

    comment = db.Column(db.String(256), nullable=False)
    rating = db.Column(db.Integer())

    vacancy = db.relationship("Vacancy", foreign_keys=[vacancy_id])
    user = db.relationship("User", foreign_keys=[user_id], backref="vacancy_ratings")

    def to_dict(self, *args, **kwargs):
        if "only" in kwargs:
            return super(VacancyRating, self).to_dict(*args, **kwargs)
        return super(VacancyRating, self).to_dict(*args, **kwargs, only=["id", "comment", "rating"])
