import os
import smtplib, ssl
from api import db, User, Vacancy, Employer
from api.services.user import get_user


def get_vacancy_by_id(vacancy_id=None, to_dict=True):
    if vacancy_id is not None:
        vacancy = db.session.query(Vacancy).get(vacancy_id)
        if vacancy is None:
            return None
        return vacancy.to_dict() if to_dict else vacancy
    return [item.to_dict() if to_dict else item for item in db.session.query(Vacancy).all()]


def create_vacancy(name, description, user_id, employer_id):
    user = get_user(user_id, to_dict=False)
    if user is None:
        raise IndexError(f"Пользователь с id {user_id} не найден")
    employer = db.session.query(Employer).get(employer_id)
    if employer is None:
        raise IndexError(f"Работодатель с id {employer_id} не найден")
    if user not in employer.users:
        raise IndexError(f"Пользователь с id {user_id} не состоит в компании {employer_id}")
    vacancy = Vacancy()
    vacancy.name = name
    vacancy.description = description
    vacancy.employer = employer

    db.session.add(vacancy)
    db.session.commit()

    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = os.environ.get("EMAIL")
    password = os.environ.get("EMAIL_PASSWORD")
    site_address = os.environ.get("APP_ADDRESS")
    message = (f"\Subject: Notify of new vacancies\n"
               f"One of your subscribed company posted a new vacancy.\n"
               f"link: http://{site_address}/employer/{vacancy.employer.id}")

    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        for sub in employer.subscribers:
            server.sendmail(sender_email, sub.email, message)
    return vacancy


def delete_vacancy(vacancy_id):
    vacancy = db.session.query(Vacancy).get(vacancy_id)
    if vacancy is None:
        raise KeyError(f"Вакансии  {vacancy_id} не существует")
    db.session.delete(vacancy)
    db.session.commit()
    return True
