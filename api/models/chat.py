from api import db
from api.models.iso8601_serializer_mixin import ISO8601SerializerMixin

users_to_chats = db.Table(
    "users_to_chats",
    db.Column("user_id", db.Integer(), db.ForeignKey("users.id"), primary_key=True),
    db.Column("chat_id", db.Integer(), db.ForeignKey("chats.id"), primary_key=True)
)


class Chat(db.Model, ISO8601SerializerMixin):
    __tablename__ = "chats"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)

    users = db.relationship("VacancyRating", secondary=users_to_chats, lazy="subquery",
                            backref=db.backref("chats", lazy=True), cascade="all")

    def to_dict(self, *args, **kwargs):
        if "only" in kwargs:
            return super(Chat, self).to_dict(*args, **kwargs)
        return super(Chat, self).to_dict(*args, **kwargs, only=["id", "name"])
