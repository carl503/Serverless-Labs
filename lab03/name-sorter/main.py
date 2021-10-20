from flask import jsonify

def entrypoint(request):
    if request.path == "/":
        data = request.json
        sorted_list = sorted(data, key=lambda k: k["last_name"])
        return jsonify(sorted_list)

    elif request.path == "/ping":
        return ('', 204)
