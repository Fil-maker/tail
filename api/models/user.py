from api import db
from api.models.employer import users_to_employers
from api.models.iso8601_serializer_mixin import ISO8601SerializerMixin


class User(db.Model, ISO8601SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(), nullable=False)

    token = db.Column(db.String(), unique=True, index=True)
    token_expiration = db.Column(db.DateTime())

    def to_dict(self, *args, **kwargs):
        if "only" in kwargs:
            return super(User, self).to_dict(*args, **kwargs)
        ans = super(User, self).to_dict(*args, **kwargs, only=["id", "name", "email"])
        ans["reputation"] = len(self.employers)
        ans["employers"] = [employer.to_dict(only=["id", "name", "description"]) for employer in self.employers]
        ans["subscriptions"] = [employer.to_dict(only=["id", "name", "description"]) for employer in self.subscriptions]
        return ans
