from pydantic import BaseModel


class RefreshTokenRequest(BaseModel):
    refresh_token: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }


class RefreshTokenResponse(BaseModel):
    success: bool
    message: str
    accessToken: str
    tokenType: str = "Bearer"
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Token refreshed successfully",
                "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "tokenType": "Bearer"
            }
        }
