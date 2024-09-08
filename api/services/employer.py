from api import db, User, Employer


def get_employer(employer_id=None, to_dict=True):
    if employer_id is not None:
        employer = db.session.query(Employer).get(employer_id)
        if employer is None:
            return None
        return employer.to_dict() if to_dict else employer
    return [item.to_dict() if to_dict else item for item in db.session.query(Employer).all()]


def create_employer(name):
    if db.session.query(Employer).filter(Employer.username == name).first() is not None:
        raise KeyError(f"Работодатель  {name} уже существует")
    employer = Employer()
    employer.username = name

    db.session.add(employer)
    db.session.commit()
    return employer


def add_user(user_id, employer_id):
    user = db.session.query(User).get(user_id)
    if user is None:
        raise IndexError(f"Пользователь с id {user_id} не найден")
    employer = db.session.query(Employer).get(employer_id)
    if employer is None:
        raise IndexError(f"Работодатель с id {user_id} не найден")
    employer.users.append(user)
    user.employers.append(employer)

    db.session.commit()
