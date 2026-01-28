"""
Exception handlers for FastAPI application
Provides centralized exception handling and response formatting
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
import logging
from datetime import datetime
import traceback
from typing import Union

from app.core.exceptions import (
    AppException,
    ErrorCode
)

# Configure logging
logger = logging.getLogger(__name__)


class ExceptionHandler:
    """Centralized exception handler"""
    
    @staticmethod
    def format_error_response(
        success: bool = False,
        error_code: Union[ErrorCode, str] = ErrorCode.INTERNAL_ERROR,
        message: str = "An unexpected error occurred",
        details: dict = None,
        timestamp: str = None,
        path: str = None
    ) -> dict:
        """Format error response consistently"""
        if timestamp is None:
            timestamp = datetime.utcnow().isoformat()
        
        return {
            "success": success,
            "timestamp": timestamp,
            "error": {
                "code": error_code,
                "message": message,
                "details": details or {},
                "path": path
            }
        }
    
    @staticmethod
    def log_exception(
        exc: Exception,
        request: Request,
        error_level: str = "error"
    ):
        """Log exception with context"""
        log_message = f"""
Exception caught:
- Type: {type(exc).__name__}
- Message: {str(exc)}
- Method: {request.method}
- Path: {request.url.path}
- Timestamp: {datetime.utcnow().isoformat()}
- Traceback:
{traceback.format_exc()}
        """
        
        if error_level == "error":
            logger.error(log_message)
        elif error_level == "warning":
            logger.warning(log_message)
        else:
            logger.info(log_message)


async def app_exception_handler(request: Request, exc: AppException):
    """Handler for custom AppException"""
    ExceptionHandler.log_exception(exc, request, error_level="warning")
    
    response_data = exc.to_dict()
    response_data["timestamp"] = datetime.utcnow().isoformat()
    response_data["path"] = request.url.path
    
    return JSONResponse(
        status_code=exc.status_code,
        content=response_data
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handler for general exceptions"""
    ExceptionHandler.log_exception(exc, request, error_level="error")
    
    response_data = ExceptionHandler.format_error_response(
        success=False,
        error_code=ErrorCode.INTERNAL_ERROR,
        message="An unexpected error occurred",
        details={"exception_type": type(exc).__name__},
        path=request.url.path
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response_data
    )


async def value_error_handler(request: Request, exc: ValueError):
    """Handler for ValueError"""
    ExceptionHandler.log_exception(exc, request, error_level="warning")
    
    response_data = ExceptionHandler.format_error_response(
        success=False,
        error_code=ErrorCode.VALIDATION_ERROR,
        message=str(exc),
        path=request.url.path
    )
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=response_data
    )


async def runtime_error_handler(request: Request, exc: RuntimeError):
    """Handler for RuntimeError"""
    ExceptionHandler.log_exception(exc, request, error_level="error")
    
    response_data = ExceptionHandler.format_error_response(
        success=False,
        error_code=ErrorCode.INTERNAL_ERROR,
        message="A runtime error occurred",
        details={"error": str(exc)},
        path=request.url.path
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response_data
    )
