from flask import jsonify


def api_success(data=None, message="OK", status=200):
    payload = {"success": True, "message": message, "data": data or {}}
    return jsonify(payload), status


def api_error(message, status=400, details=None):
    payload = {"success": False, "error": message}
    if details:
        payload["details"] = details
    return jsonify(payload), status
