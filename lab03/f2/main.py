from flask import jsonify
import random

def entrypoint(request):
    if request.path == "/":
        data = request.json
        random.shuffle(data)
        return jsonify(data)

    elif request.path == "/ping":
        return ('', 204)
