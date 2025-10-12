from flask import jsonify

class Response:
    @staticmethod
    def success(data=None, message="Operation completed successfully"):
        resp = {"success": True, "message": message}
        if data is not None:
            resp["data"] = data
        return jsonify(resp), 201

    @staticmethod
    def error(message="An error occurred"):
        return jsonify({"success": False, "message": message}), 400
