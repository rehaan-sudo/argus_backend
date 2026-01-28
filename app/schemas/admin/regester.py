from pydantic import BaseModel, EmailStr


class AdminRegisterRequest(BaseModel):
    name: str
    password: str
    email: EmailStr
    organization_name: str
    phone: str


class AdminRegisterResponse(BaseModel):
    message: str
    access_token: str
    refresh_token: str
