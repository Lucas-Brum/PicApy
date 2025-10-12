from flask import jsonify, make_response

class ResponseHandler:
    @staticmethod
    def success(data=None, message="Operação realizada com sucesso", status_code=200):
        body = {
            "success": True,
            "message": message
        }
        if data is not None:
            body["data"] = data
        return make_response(jsonify(body), status_code)

    @staticmethod
    def created(data=None, message="Recurso criado com sucesso"):
        return ResponseHandler.success(data=data, message=message, status_code=201)

    @staticmethod
    def error(message="Erro interno do servidor", status_code=400, error_code=None, details=None):
        body = {
            "success": False,
            "message": message
        }
        if error_code:
            body["error_code"] = error_code
        if details:
            body["details"] = details
        return make_response(jsonify(body), status_code)
