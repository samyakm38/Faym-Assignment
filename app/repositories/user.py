from sqlalchemy.orm import Session

from app.models.user import User
from .base import BaseRepository
from sqlalchemy import select



class UserRepository(BaseRepository):

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.scalar(
            select(User).where(User.id == user_id)
        )

    def save(self, user: User) -> None:
        self.db.add(user)
        self.db.flush()