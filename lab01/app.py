import flask

import main


app = flask.Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    return main.entrypoint(flask.request)