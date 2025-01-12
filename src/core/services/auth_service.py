from infrastructure.repositories.user_repository import UserRepository
import bcrypt



class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def authenticate_user(self, username: str, password: str):
        user = self.user_repository.get_user_by_username(username)

        if user and user.verify_password():
            return user

        return None


class User:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = self.hash_password(password)

    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)