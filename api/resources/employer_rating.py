from flask import jsonify
from flask_restful import Resource, abort
from flask_restful.reqparse import RequestParser

from api.services.employer_rating import get_employer_rating, create_employer_rating


class EmployerRatingResource(Resource):
    def get(self, employer_rating_id):
        employer_rating = get_employer_rating(employer_rating_id)
        if employer_rating is None:
            abort(404, success=False, message=f"Отзыв {employer_rating_id} не найден")
        return jsonify({"success": True, "employer_rating": employer_rating})


class EmployerRatingListResource(Resource):
    def get(self):
        return jsonify({"success": True, "employers": get_employer_rating()})

    def post(self):
        parser = RequestParser()
        parser.add_argument("user_id", type=int, required=True)
        parser.add_argument("employer_id", type=int, required=True)
        parser.add_argument("comment", required=True)
        parser.add_argument("rating", type=int, required=True)

        kwargs = parser.parse_args(strict=True)
        try:
            employer_rating = create_employer_rating(**kwargs)
        except KeyError as e:
            return jsonify({"success": False, "message": str(e)}), 400
        else:
            return jsonify({"success": True, "employer_rating": employer_rating.to_dict()})

