from flask import jsonify
from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser

from api.services.reply import get_reply, create_reply, delete_reply, get_replies_from_vacancy_id


class ReplyResource(Resource):
    def get(self, reply_id):
        reply = get_reply(reply_id)
        if reply is None:
            abort(404, success=False, message=f"Отклик {reply_id} не найден")
        return jsonify({"success": True, "reply": reply})

    def delete(self, reply_id):
        delete_reply(reply_id)
        return jsonify({"success": True})


class ReplyListResource(Resource):
    def get(self):
        parser = RequestParser()
        parser.add_argument("vacancy_id", type=int, required=False)
        kwargs = parser.parse_args(strict=True)
        if kwargs["vacancy_id"]:
            try:
                replies = get_replies_from_vacancy_id(**kwargs)
            except Exception as e:
                return jsonify({"success": False, "message": str(e), "error_code": 400})
            else:
                return jsonify({"success": True, "replies": replies})
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
        except Exception as e:
            return jsonify({"success": False, "message": str(e), "error_code": 400})
        else:
            return jsonify({"success": True, "reply": reply.to_dict()})
