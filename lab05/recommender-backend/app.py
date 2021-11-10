import flask
import main
import os
from flask_cors import CORS


app = flask.Flask(__name__)
CORS(app)


@app.route("/", methods=["POST", "GET"])
@app.route("/recommend", methods=["GET"])
def index():
    return main.entrypoint(flask.request)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT", "8080"))