from api import db, User, Employer, Vacancy, Reply


def get_reply(reply_id=None, to_dict=True):
    if reply_id is not None:
        reply = db.session.query(Reply).get(reply_id)
        if reply is None:
            return None
        return reply.to_dict() if to_dict else reply
    return [item.to_dict() if to_dict else item for item in db.session.query(Reply).all()]


def create_reply(user_id, vacancy_id, resume_link, cv_link):
    if db.session.query(Reply).filter(Reply.vacancy_id == vacancy_id).filter(Reply.user_id == user_id).first() is not None:
        raise KeyError(f"Вы уже откликались на эту должность")
    user = db.session.query(User).get(user_id)
    if user is None:
        raise KeyError(f"Пользователя не существует")
    vacancy = db.session.query(Vacancy).get(vacancy_id)
    if vacancy is None:
        raise KeyError(f"Вакансии не существует")
    reply = Reply()
    reply.user_id = user_id
    reply.vacancy_id = vacancy_id
    reply.user = user
    reply.vacancy = vacancy

    reply.status = None
    reply.resume_link = resume_link
    reply.cv_link = cv_link

    db.session.add(reply)
    db.session.commit()
    return reply
