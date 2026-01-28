"""
Global Exception Handling Module
Defines custom exceptions for the application
"""

from typing import Optional, Any, Dict
from enum import Enum


class ErrorCode(str, Enum):
    """Error codes for consistent error identification"""
    VALIDATION_ERROR = "VALIDATION_ERROR"
    AUTHENTICATION_ERROR = "AUTHENTICATION_ERROR"
    AUTHORIZATION_ERROR = "AUTHORIZATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"
    CAMERA_ERROR = "CAMERA_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"
    VPN_CONFIG_ERROR = "VPN_CONFIG_ERROR"
    ONBOARDING_ERROR = "ONBOARDING_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    EMAIL_EXISTS = "EMAIL_EXISTS"
    INVALID_REQUEST = "INVALID_REQUEST"


class AppException(Exception):
    """Base exception for the application"""
    
    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.INTERNAL_ERROR,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for response"""
        return {
            "success": False,
            "error": {
                "code": self.error_code,
                "message": self.message,
                "details": self.details
            }
        }


class ValidationError(AppException):
    """Raised when request validation fails"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.VALIDATION_ERROR,
            status_code=400,
            details=details
        )


class AuthenticationError(AppException):
    """Raised when authentication fails"""
    def __init__(self, message: str = "Authentication failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.AUTHENTICATION_ERROR,
            status_code=401,
            details=details
        )


class AuthorizationError(AppException):
    """Raised when user is not authorized"""
    def __init__(self, message: str = "Not authorized", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.AUTHORIZATION_ERROR,
            status_code=403,
            details=details
        )


class NotFoundError(AppException):
    """Raised when resource is not found"""
    def __init__(self, resource: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"{resource} not found",
            error_code=ErrorCode.NOT_FOUND,
            status_code=404,
            details=details
        )


class ConflictError(AppException):
    """Raised when there's a conflict (e.g., duplicate entry)"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.CONFLICT,
            status_code=409,
            details=details
        )


class CameraError(AppException):
    """Raised when camera operation fails"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.CAMERA_ERROR,
            status_code=400,
            details=details
        )


class DatabaseError(AppException):
    """Raised when database operation fails"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.DATABASE_ERROR,
            status_code=500,
            details=details
        )


class VPNConfigError(AppException):
    """Raised when VPN configuration fails"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.VPN_CONFIG_ERROR,
            status_code=400,
            details=details
        )


class OnboardingError(AppException):
    """Raised when onboarding operation fails"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.ONBOARDING_ERROR,
            status_code=400,
            details=details
        )


class EmailExistsError(AppException):
    """Raised when email already exists"""
    def __init__(self, email: str):
        super().__init__(
            message="Email already registered",
            error_code=ErrorCode.EMAIL_EXISTS,
            status_code=409,
            details={"email": email}
        )


class InvalidRequestError(AppException):
    """Raised when request is invalid"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.INVALID_REQUEST,
            status_code=400,
            details=details
        )
