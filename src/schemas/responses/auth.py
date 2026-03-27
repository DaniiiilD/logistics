from pydantic import BaseModel, ConfigDict
    
class UserResponse(BaseModel):
    id: int
    email: str
    role: str

class LoginResponse(BaseModel):
    id: int
    email: str
    role: str
    
    model_config = ConfigDict(from_attributes=True)
    