

from pydantic import BaseModel


class CameraOnboardingRequest(BaseModel):
    branch_name: str
    company_name: str
    typeoforganization: str 
    phone: str
    country: str
    goal : str

    use_cases_list: list[str]

    vpn_user_name: str
    vpn_password: str
    site_name: str
    # vpn path file upload in file_upload variable
    file_upload:str   

    port : int
    camera_user_name: str
    camera_password: str

    camera_name: str
    ip_address: str
    camera_zone: str