from api import db, User, Employer


def get_employer(employer_id=None, to_dict=True):
    if employer_id is not None:
        employer = db.session.query(Employer).get(employer_id)
        if employer is None:
            return None
        return employer.to_dict() if to_dict else employer
    return [item.to_dict() if to_dict else item for item in db.session.query(Employer).all()]


def create_employer(name, description):
    if db.session.query(Employer).filter(Employer.name == name).first() is not None:
        raise KeyError(f"Работодатель  {name} уже существует")
    employer = Employer(name=name, description=description)
    # employer.username = name
    # employer.description = description

    db.session.add(employer)
    db.session.commit()
    return employer


def add_user_to_employer(user_id, employer_id):
    user = db.session.query(User).get(user_id)
    if user is None:
        raise IndexError(f"Пользователь с id {user_id} не найден")
    employer = db.session.query(Employer).get(employer_id)
    if employer is None:
        raise IndexError(f"Работодатель с id {employer_id} не найден")
    if user in employer.users:
        raise IndexError(f"Пользователь уже в добавлен к работодателю")
    employer.users.append(user)
    db.session.commit()
    return employer


def subscribe_user_to_employer(user_id, employer_id):
    user = db.session.query(User).get(user_id)
    if user is None:
        raise IndexError(f"Пользователь с id {user_id} не найден")
    employer = db.session.query(Employer).get(employer_id)
    if employer is None:
        raise IndexError(f"Работодатель с id {employer} не найден")
    if user in employer.subscribers:
        raise IndexError(f"Вы уже подписаны на этого работодателя")
    employer.subscribers.append(user)
    db.session.commit()
    return employer


def unsubscribe_user_from_employer(user_id, employer_id):
    user = db.session.query(User).get(user_id)
    if user is None:
        raise IndexError(f"Пользователь с id {user_id} не найден")
    employer = db.session.query(Employer).get(employer_id)
    if employer is None:
        raise IndexError(f"Работодатель с id {employer} не найден")
    if user not in employer.subscribers:
        raise IndexError(f"Вы на подписаны этого работодателя")
    employer.subscribers.remove(user)
    db.session.commit()
    return employer
