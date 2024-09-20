import os
import smtplib, ssl
from api import db, User, Employer, Vacancy, Reply
from api.services.vacancy import get_vacancy_by_id


def get_reply(reply_id=None, to_dict=True):
    if reply_id is not None:
        reply = db.session.query(Reply).get(reply_id)
        if reply is None:
            return None
        return reply.to_dict() if to_dict else reply
    return [item.to_dict() if to_dict else item for item in db.session.query(Reply).all()]


def create_reply(user_id, vacancy_id, resume_link, cv_link):
    if db.session.query(Reply).filter(Reply.vacancy_id == vacancy_id).filter(
            Reply.user_id == user_id).first() is not None:
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


def delete_reply(reply_id):
    reply = get_reply(reply_id, to_dict=False)
    db.session.delete(reply)
    db.session.commit()
    return True


def get_replies_from_vacancy_id(vacancy_id):
    vacancy = get_vacancy_by_id(vacancy_id, to_dict=False)
    replies = vacancy.replies

    return [reply.to_dict() for reply in replies]


def apply_reply(reply_id):
    reply = get_reply(reply_id, to_dict=False)
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = os.environ.get("EMAIL")
    password = os.environ.get("EMAIL_PASSWORD")
    site_address = os.environ.get("APP_ADDRESS")
    message = (f"\Subject: Notify of success resume\n"
               f"One of your resume was approved.\n"
               f"link: http://{site_address}/employer/{reply.vacancy.employer.id}")

    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, reply.user.email, message)
    if reply.status is not None:
        raise KeyError(f"Заявка уже одобрена. Заявитель уведомлен")
    reply.status = "Одобрено"

    db.session.commit()
    return reply
