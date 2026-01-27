class  AdminRegisterRequest:
    username: str
    password: str
    email: str
    organization_id: int


class  AdminRegisterResponse:
    message: str
    access_token: str
    token_type: str
    user: dict
   