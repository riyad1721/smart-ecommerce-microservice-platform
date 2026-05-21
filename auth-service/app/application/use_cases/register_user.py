from fastapi import HTTPException, status

from app.core.security import hash_password
from app.infrastructure.repositories.user_repository import UserRepository


class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, full_name: str, email: str, password: str):
        existing_user = self.user_repository.get_by_email(email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists with this email"
            )

        hashed_password = hash_password(password)

        return self.user_repository.create(
            full_name=full_name,
            email=email,
            hashed_password=hashed_password
        )