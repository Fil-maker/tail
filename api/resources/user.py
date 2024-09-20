from flask import jsonify
from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser

from api.services.user import get_user, create_user


class UserResource(Resource):
    def get(self, user_id):
        user = get_user(user_id)
        if user is None:
            abort(404, success=False, message=f"Пользователь {user_id} не найден")
        return jsonify({"success": True, "user": user})


class UserListResource(Resource):
    def get(self):
        return jsonify({"success": True, "users": get_user()})

    def post(self):
        parser = RequestParser()
        parser.add_argument("email", required=True)
        parser.add_argument("username", required=True)
        parser.add_argument("password", required=True)

        kwargs = parser.parse_args(strict=True)
        try:
            user, token, expires = create_user(**kwargs)
        except KeyError as e:
            return jsonify({"success": False, "message": str(e), "error_code":400})
        else:
            return jsonify({"success": True, "user": user.to_dict(),
                            "authToken": {"token": token,
                                          "expires": expires}})
