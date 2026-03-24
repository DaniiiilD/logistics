from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.orm.models.user import User
from src.orm.repositories.base import BaseRepository

class UserRepository(BaseRepository):
    
    model = User
        
    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).filter(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def create(self, email: str, hashed_password: str, role: str) -> User:
        user = User(email=email,
                    hashed_password=hashed_password,
                    role=role)
        self.session.add(user)
        await self.session.flush()
        return user