from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.orm.models.user import User
from src.orm.repositories.base import BaseRepository
from src.orm.database import async_session_factory

class UserRepository(BaseRepository):
    
    model = User
        
    async def get_by_email(self, email: str) -> User | None:
        async with async_session_factory() as session:
            result = await session.execute(
                select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def create(self, email: str, hashed_password: str, role: str) -> User:
        async with async_session_factory() as session:
            user = User(email=email,
                    hashed_password=hashed_password,
                    role=role)
        session.add(user)
        await session.commit()
        await session.flush()
        return user