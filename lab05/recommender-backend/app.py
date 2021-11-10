import flask
import main
import os


app = flask.Flask(__name__)


@app.route("/", methods=["POST", "GET"])
@app.route("/recommend", methods=["GET"])
def index():
    return main.entrypoint(flask.request)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT", "8080"))