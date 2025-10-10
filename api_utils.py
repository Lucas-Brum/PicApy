from flask import jsonify

class Validations:
    def __init__(self, user, email, password):
        self.user = user
        self.email = email
        self.password = password
        
    def validate_user_data(self):
        # Validação mínima
        if not self.user or not self.email or not self.password:
            return jsonify({"error": "Campos obrigatórios: user, email, password"}), 400
        

class Response:
    def __init__(self, user, email):
        self.user = user
        self.email = email

    def create_response(self):
        return jsonify({
            "message": "Usuário recebido com sucesso",
            "user": self.user,
            "email": self.email
    }), 201