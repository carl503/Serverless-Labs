from flask import jsonify
import random

def entrypoint(request):
    if request.path == "/":
        
        data = f"{request.json['first_name']} {request.json['last_name']}"
        shuffled_list = random.shuffle(data)
        return jsonify(shuffled_list)

    elif request.path == "/ping":
        return ('', 204)
