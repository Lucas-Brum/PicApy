import bcrypt


class Security:
    @staticmethod
    def hash_password(password: str) -> bytes:
        """Gera um hash seguro da senha usando bcrypt."""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    @staticmethod
    def verify_password(password: str, hashed: bytes) -> bool:
        """Verifica se a senha corresponde ao hash armazenado."""
        return bcrypt.checkpw(password.encode("utf-8"), hashed)
