import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

dotenv_path = os.path.join(os.path.dirname(__file__), ".", ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    raise FileNotFoundError(".env file not found")

app = Flask(__name__)
pg_user = os.environ.get("PG_USER")
pg_pass = os.environ.get("PG_PASS")
pg_host = os.environ.get("PG_HOST")
db_name = os.environ.get("DB_NAME")
app.config["SECRET_KEY"] = os.environ.get("API_SECRET")
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{pg_user}:{pg_pass}@{pg_host}/{db_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app, session_options={"autoflush": False})
from api.models import *

with app.app_context():
    db.create_all()
# db.init_app(app)

api = Api(app)
migrate = Migrate(app, db)


from api.resources.user import UserResource, UserListResource

api.add_resource(UserResource, "/api/users/<int:user_id>")
api.add_resource(UserListResource, "/api/users")

from api.resources.employer import EmployerResource, EmployerListResource

api.add_resource(EmployerResource, "/api/employers/<int:employer_id>")
api.add_resource(EmployerListResource, "/api/employers")

from api.resources.vacancy import VacancyResource, VacancyListResource

api.add_resource(VacancyResource, "/api/vacancies/<int:vacancy_id>")
api.add_resource(VacancyListResource, "/api/vacancies")

from api.resources.reply import ReplyResource, ReplyListResource

api.add_resource(ReplyResource, "/api/replies/<int:reply_id>", methods=["GET", "DELETE"])
api.add_resource(ReplyListResource, "/api/replies")

from api import controllers
