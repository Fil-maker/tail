import os
# import api
from api import app


def run():
    app.run(host=os.environ.get("API_HOST"),
            port=os.environ.get("API_PORT"),
            debug=bool(int(os.environ.get("API_DEBUG"))))


if __name__ == '__main__':
    run()
