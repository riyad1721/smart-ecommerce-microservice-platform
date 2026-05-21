from app.application.use_cases.login_user import LoginUserUseCase
from app.application.use_cases.register_user import RegisterUserUseCase
from app.infrastructure.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, full_name: str, email: str, password: str):
        use_case = RegisterUserUseCase(self.user_repository)

        return use_case.execute(
            full_name=full_name,
            email=email,
            password=password
        )

    def login_user(self, email: str, password: str) -> str:
        use_case = LoginUserUseCase(self.user_repository)

        return use_case.execute(
            email=email,
            password=password
        )