from flask import jsonify
from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser

from api.services.employer import get_employer, create_employer, add_user_to_employer


class EmployerResource(Resource):
    def get(self, employer_id):
        employer = get_employer(employer_id)
        if employer is None:
            abort(404, success=False, message=f"Работодатель {employer_id} не найден")
        return jsonify({"success": True, "employer": employer})

    def put(self, employer_id):
        parser = RequestParser()
        parser.add_argument("user_id", required=True)

        kwargs = parser.parse_args(strict=True)
        try:
            response = add_user_to_employer(kwargs["user_id"], employer_id)
        except KeyError as e:
            return jsonify({"success": False, "message": str(e), "error_code": 400})
        else:
            return jsonify({"success": True})


class EmployerListResource(Resource):
    def get(self):
        return jsonify({"success": True, "employers": get_employer()})

    def post(self):
        parser = RequestParser()
        parser.add_argument("name", required=True)

        kwargs = parser.parse_args(strict=True)
        try:
            employer = create_employer(**kwargs)
        except KeyError as e:
            return jsonify({"success": False, "message": str(e)}), 400
        else:
            return jsonify({"success": True, "employer": employer.to_dict()})
