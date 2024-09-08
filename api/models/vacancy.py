from api import db
from api.models.iso8601_serializer_mixin import ISO8601SerializerMixin

ratings_to_vacancies = db.Table(
    "ratings_to_vacancies",
    db.Column("vacancy_id", db.Integer(), db.ForeignKey("vacancies.id"), primary_key=True),
    db.Column("rating_id", db.Integer(), db.ForeignKey("vacancy_ratings.id"), primary_key=True)
)


class Vacancy(db.Model, ISO8601SerializerMixin):
    __tablename__ = "vacancies"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    employer_id = db.Column(db.Integer(), db.ForeignKey("employers.id"))
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256), nullable=False)

    employer = db.relationship("Employer", foreign_keys=[employer_id], backref="vacancies")
    vacancy_ratings = db.relationship("VacancyRating", secondary=ratings_to_vacancies, lazy="subquery",
                                      backref=db.backref("employers", lazy=True), cascade="all")

    def to_dict(self, *args, **kwargs):
        if "only" in kwargs:
            return super(Vacancy, self).to_dict(*args, **kwargs)
        return super(Vacancy, self).to_dict(*args, **kwargs, only=["id", "name"])
