from api import db, User, EmployerRating, Employer


def get_employer_rating(employer_rating_id=None, to_dict=True):
    if employer_rating_id is not None:
        employer_rating = db.session.query(EmployerRating).get(employer_rating_id)
        if employer_rating is None:
            return None
        return employer_rating.to_dict() if to_dict else employer_rating
    return [item.to_dict() if to_dict else item for item in db.session.query(EmployerRating).all()]


def create_employer_rating(user_id, employer_id, comment, rating):
    if db.session.query(EmployerRating).filter(EmployerRating.employer_id == employer_id).filter(EmployerRating.user_id == user_id).first() is not None:
        raise KeyError(f"Оценка уже имеется")
    employer_rating = EmployerRating()
    user = db.session.query(User).get(user_id)
    if user is None:
        raise KeyError(f"Пользователя не существует")
    employer = db.session.query(Employer).get(employer_id)
    if employer is None:
        raise KeyError(f"Работодателя не существует")
    employer_rating.user_id = user_id
    employer_rating.employer_id = employer_id
    employer_rating.employer = employer
    employer_rating.user = user

    employer_rating.comment = comment
    employer_rating.rating = rating

    db.session.add(employer_rating)
    db.session.commit()
    return employer_rating
