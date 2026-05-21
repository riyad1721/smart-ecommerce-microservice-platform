from sqlalchemy.orm import Session

from app.infrastructure.database.models import UserModel


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> UserModel | None:
        return self.db.query(UserModel).filter(UserModel.email == email).first()

    def get_by_id(self, user_id: str) -> UserModel | None:
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def create(self, full_name: str, email: str, hashed_password: str) -> UserModel:
        user = UserModel(
            full_name=full_name,
            email=email,
            hashed_password=hashed_password
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user