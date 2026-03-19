from pydantic import BaseModel
    
class UserResponse(BaseModel):
    id: int
    email: str
    role: str

class LoginResponse(BaseModel):
    id: int
    email: str
    role: str
    