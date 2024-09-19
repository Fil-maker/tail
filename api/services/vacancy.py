from api import db, User, Vacancy


def get_vacancy_by_id(vacancy_id=None, to_dict=True):
    if vacancy_id is not None:
        vacancy = db.session.query(Vacancy).get(vacancy_id)
        if vacancy is None:
            return None
        return vacancy.to_dict() if to_dict else vacancy
    return [item.to_dict() if to_dict else item for item in db.session.query(Vacancy).all()]


def create_vacancy(name, description, employer_id):
    employer = db.session.query(Vacancy).get(employer_id)
    if employer is None:
        raise IndexError(f"Работодатель с id {employer_id} не найден")
    vacancy = Vacancy()
    vacancy.name = name
    vacancy.description = description
    vacancy.employer = employer
    employer.vacancies.append(vacancy)

    db.session.add(vacancy)
    db.session.commit()
    return vacancy


def delete_vacancy(vacancy_id):
    vacancy = db.session.query(Vacancy).get(vacancy_id)
    if vacancy is None:
        raise KeyError(f"Вакансии  {vacancy_id} не существует")
    db.session.delete(vacancy)
    db.session.commit()
    return True
