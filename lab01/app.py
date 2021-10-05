import flask
import main


app = flask.Flask(__name__)


@app.route("/", methods=["POST", "GET"])
@app.route("/recommend", methods=["GET"])
def index():
    return main.entrypoint(flask.request)