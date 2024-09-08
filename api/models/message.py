from api import db
from api.models.iso8601_serializer_mixin import ISO8601SerializerMixin


class Message(db.Model, ISO8601SerializerMixin):
    __tablename__ = "messages"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    chat_id = db.Column(db.Integer(), db.ForeignKey("chats.id"))
    content = db.Column(db.String(), nullable=False)

    user = db.relationship("User", foreign_keys=[user_id])
    chat = db.relationship("User", foreign_keys=[chat_id], backref="messages")

    def to_dict(self, *args, **kwargs):
        if "only" in kwargs:
            return super(Message, self).to_dict(*args, **kwargs)
        return super(Message, self).to_dict(*args, **kwargs, only=["id", "content"])
