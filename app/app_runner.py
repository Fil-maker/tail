import os
from app import app
from app.test.user import test


# from flask_socketio import SocketIO


def run():
    app.run(host=os.environ.get("APP_HOST"),
            port=os.environ.get("APP_PORT"),
            debug=bool(int(os.environ.get("APP_DEBUG"))))
    # socketio.run(app)


if __name__ == '__main__':
    run()
    # test()
