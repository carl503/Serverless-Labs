from flask import jsonify
import random

def entrypoint(request):
    if request.path == "/":
        data = request.json
        shuffled_list = random.shuffle(data)
        return shuffled_list

    elif request.path == "/ping":
        return ('', 204)
