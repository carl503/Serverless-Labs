from flask import jsonify

def entrypoint(request):
    if request.path == "/":
        data = request.json
        return jsonify(sorted(data))
