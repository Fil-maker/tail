from api import db
from api.models.iso8601_serializer_mixin import ISO8601SerializerMixin

users_to_employers = db.Table(
    "users_to_employers",
    db.Column("user_id", db.Integer(), db.ForeignKey("users.id"), primary_key=True),
    db.Column("employer_id", db.Integer(), db.ForeignKey("employers.id"), primary_key=True)
)

ratings_to_employers = db.Table(
    "ratings_to_employers",
    db.Column("employer_id", db.Integer(), db.ForeignKey("employers.id"), primary_key=True),
    db.Column("rating_id", db.Integer(), db.ForeignKey("employer_ratings.id"), primary_key=True)
)


class Employer(db.Model, ISO8601SerializerMixin):
    __tablename__ = "employers"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)

    users = db.relationship("User", secondary=users_to_employers, lazy="subquery",
                            backref=db.backref("employers", lazy=True), cascade="all")
    ratings = db.relationship("EmployerRating", secondary=ratings_to_employers, lazy="subquery",
                              backref=db.backref("employers", lazy=True), cascade="all")

    def to_dict(self, *args, **kwargs):
        if "only" in kwargs:
            return super(Employer, self).to_dict(*args, **kwargs)
        ans = super(Employer, self).to_dict(*args, **kwargs, only=["id", "name"])
        ans["ratings"] = []
        ans["score"] = sum(map(lambda x: x.rating, self.ratings)) / len(self.ratings)
        for rating in self.ratings:
            ans["ratings"].append(rating.to_dict())
        return ans
