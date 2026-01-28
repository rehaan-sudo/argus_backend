from pydantic import BaseModel, EmailStr
from pydantic import  field_validator

class AdminRegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str
    phone: str
    organization_name: str

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, confirm_password, info):
        password = info.data.get("password")
        if password != confirm_password:
            raise ValueError("Password and confirm password do not match")
        return confirm_password


