from flask import jsonify
from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser

from api.services.replies import get_reply, create_reply


class ReplyResource(Resource):
    def get(self, reply_id):
        reply = get_reply(reply_id)
        if reply is None:
            abort(404, success=False, message=f"Отклик {reply_id} не найден")
        return jsonify({"success": True, "reply": reply})


class ReplyListResource(Resource):
    def get(self):
        return jsonify({"success": True, "replies": get_reply()})

    def post(self):
        parser = RequestParser()
        parser.add_argument("user_id", type=int, required=True)
        parser.add_argument("vacancy_id", type=int, required=True)
        parser.add_argument("resume_link", required=True)
        parser.add_argument("cv_link", required=True)

        kwargs = parser.parse_args(strict=True)
        try:
            reply = create_reply(**kwargs)
        except KeyError as e:
            return jsonify({"success": False, "message": str(e)}), 400
        else:
            return jsonify({"success": True, "reply": reply.to_dict()})

