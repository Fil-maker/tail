from flask import jsonify
from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser

from api.services.chat import get_chat, create_chat


class ChatResource(Resource):
    def get(self, chat_id):
        chat = get_chat(chat_id)
        if chat is None:
            abort(404, success=False, message=f"Чат {chat_id} не найден")
        return jsonify({"success": True, "chat": chat})


class ChatListResource(Resource):
    def get(self):
        return jsonify({"success": True, "chats": get_chat()})

    def post(self):
        parser = RequestParser()
        parser.add_argument("name", required=True)

        kwargs = parser.parse_args(strict=True)
        try:
            chat = create_chat(**kwargs)
        except KeyError as e:
            return jsonify({"success": False, "message": str(e)}), 400
        else:
            return jsonify({"success": True, "chat": chat.to_dict()})

