from flask import jsonify
import numpy as np

def entrypoint(request):
    if request.path == "/":
        data = request.json
        np.random.shuffle(data)
        return jsonify(data)

    elif request.path == "/ping":
        return ('', 204)
