from pydantic import BaseModel, Field, IPvAnyAddress
from typing import List, Optional


# 🔹 Organization / Company Info
class OrganizationInfo(BaseModel):
    company_name: str = Field(..., example="ABC Industries")
    organization_type: str = Field(..., example="Manufacturing")
    branch_name: str = Field(..., example="Delhi Plant")
    country: str = Field(..., example="India")
    contact_phone: str = Field(..., min_length=10, max_length=15)
    goal: str = Field(..., example="AI Camera Monitoring")


# 🔹 Use Case Info
class UseCaseInfo(BaseModel):
    use_case_ids: List[int] = Field(..., example=[1, 2, 3])


# 🔹 VPN Configuration
class VPNConfig(BaseModel):
    vpn_username: str
    vpn_password: str
    site_name: str
    vpn_config_file_path: Optional[str] = Field(
        None, example="/uploads/vpn/config.ovpn"
    )


# 🔹 Camera Configuration
class CameraConfig(BaseModel):
    camera_name: str
    ip_address: IPvAnyAddress
    port: int = Field(..., ge=1, le=65535)
    username: str
    password: str
    camera_zone: str = Field(..., example="Entry Gate")


# 🔹 Final Onboarding Request
class CameraOnboardingRequest(BaseModel):
    organization: OrganizationInfo
    use_cases: UseCaseInfo
    vpn: VPNConfig
    camera: CameraConfig
