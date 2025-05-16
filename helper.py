from flask import jsonify, make_response

def send_response(status_code, data=''):
    payload = {
        'status_code': status_code,
        'data': data
    }
    return make_response(jsonify(payload), status_code)
