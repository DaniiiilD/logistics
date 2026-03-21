from src.orm.models.user import User
from src.orm.repositories.base import BaseRepository

class UserRepository(BaseRepository):
    
    model = User
        
    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()
    
    def create(self, email: str, hashed_password: str, role: str) -> User:
        user = User(email=email,
                    hashed_password=hashed_password,
                    role=role)
        self.db.add(user)
        self.db.flush()
        return user