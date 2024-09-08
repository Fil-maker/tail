from api import db
from api.models.iso8601_serializer_mixin import ISO8601SerializerMixin


class UserRating(db.Model, ISO8601SerializerMixin):
    __tablename__ = "user_ratings"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    employer_id = db.Column(db.Integer(), db.ForeignKey("employers.id"))

    comment = db.Column(db.String(256), nullable=False)
    rating = db.Column(db.Integer())

    employer = db.relationship("Employer", foreign_keys=[employer_id], backref="user_ratings")
    user = db.relationship("User", foreign_keys=[user_id], backref="ratings_by_users")

    def to_dict(self, *args, **kwargs):
        if "only" in kwargs:
            return super(UserRating, self).to_dict(*args, **kwargs)
        return super(UserRating, self).to_dict(*args, **kwargs, only=["id", "comment", "rating"])
