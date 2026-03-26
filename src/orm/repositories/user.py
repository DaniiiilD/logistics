from src.orm.models.user import User
from src.orm.repositories.base import BaseRepository
from sqlalchemy import select


class UserRepository(BaseRepository):
    
    model = User
        
    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()