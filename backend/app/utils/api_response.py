from flask import jsonify


def success_response(message="Success", data=None, meta=None, status_code=200):
    payload = {"success": True, "message": message, "data": data if data is not None else {}}
    if meta is not None:
        payload["meta"] = meta
    return jsonify(payload), status_code


def error_response(message="Something went wrong", errors=None, status_code=400):
    payload = {"success": False, "message": message, "data": {}}
    if errors is not None:
        payload["errors"] = errors
    return jsonify(payload), status_code
