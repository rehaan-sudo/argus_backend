from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    success: bool
    message: str
    accessToken: str
    refreshToken: str = None
    tokenType: str = "Bearer"
    user: dict = None
