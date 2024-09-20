from flask import jsonify
from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser

from api.services.vacancy import get_vacancy_by_id, create_vacancy


class VacancyResource(Resource):
    def get(self, vacancy_id):
        parser = RequestParser()
        parser.add_argument("name")
        parser.add_argument("description")

        kwargs = parser.parse_args(strict=True)

        vacancy = get_vacancy_by_id(vacancy_id)
        if vacancy is None:
            abort(404, success=False, message=f"Вакансия {vacancy_id} не найден")
        return jsonify({"success": True, "vacancy": vacancy})


class VacancyListResource(Resource):
    def get(self):
        return jsonify({"success": True, "vacancies": get_vacancy_by_id()})

    def post(self):
        parser = RequestParser()
        parser.add_argument("user_id", type=int, required=True)
        parser.add_argument("employer_id", type=int, required=True)
        parser.add_argument("name", required=True)
        parser.add_argument("description", required=True)

        kwargs = parser.parse_args(strict=True)
        try:
            vacancy = create_vacancy(**kwargs)
        except Exception as e:
            return jsonify({"success": False, "message": str(e), "error_code": 400})
        else:
            return jsonify({"success": True, "vacancy": vacancy.to_dict()})

