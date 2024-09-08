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
# db.create_all()
db.init_app(app)

api = Api(app)
migrate = Migrate(app, db)

usr = User(name="name", email="email")
emp = Employer(name="comp")
empRat = EmployerRating(comment="super cool", rating=10)
emp.ratings.append(empRat)
emp.users.append(usr)
usr.employer_ratings.append(empRat)
print(emp.users, emp.ratings, usr.employer_ratings)
# with app.app_context():

# from api.resources.users import UserResource, UserListResource
# api.add_resource(UserResource, "/api/users/<int:user_id>")
# api.add_resource(UserListResource, "/api/users")
#
# from api.resources.games import GameResource, GameListResource
# api.add_resource(GameResource, "/api/games/<int:game_id>")
# api.add_resource(GameListResource, "/api/games")
#
# from api.resources.requests import RequestResource, RequestListResource
# api.add_resource(RequestResource, "/api/requests/<int:request_id>")
# api.add_resource(RequestListResource, "/api/requests")
#
# from api.resources.player_teams import PlayerTeamResource, PlayerTeamListResource
# api.add_resource(PlayerTeamResource, "/api/player_teams/<int:player_team_id>")
#
# from api.resources.engine.grants import GrantResource, GrantListResource
# api.add_resource(GrantResource, "/api/engine/grants/<int:grant_id>")
# api.add_resource(GrantListResource, "/api/engine/grants")
#
# from api.resources.engine.scientists import ScientistResource, ScientistListResource
# api.add_resource(ScientistResource, "/api/engine/scientists/<int:grant_id>")
# api.add_resource(ScientistListResource, "/api/engine/scientists")
#

from api import controllers
