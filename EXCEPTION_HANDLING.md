# Exception Handling System Documentation

## Overview
A centralized, global exception handling system has been implemented for the Argus Backend application. This system ensures consistent error responses, comprehensive logging, and proper HTTP status codes across all API endpoints.

---

## Files Created/Modified

### 1. **app/core/exceptions.py** (NEW)
Defines all custom exception classes for the application.

#### Exception Classes:

| Exception Class | HTTP Status | Error Code | Use Case |
|---|---|---|---|
| `AppException` | - | - | Base exception for all custom exceptions |
| `ValidationError` | 400 | VALIDATION_ERROR | Request validation failures |
| `AuthenticationError` | 401 | AUTHENTICATION_ERROR | Authentication failures |
| `AuthorizationError` | 403 | AUTHORIZATION_ERROR | Authorization failures |
| `NotFoundError` | 404 | NOT_FOUND | Resource not found |
| `ConflictError` | 409 | CONFLICT | Duplicate entries |
| `CameraError` | 400 | CAMERA_ERROR | Camera validation/connection issues |
| `DatabaseError` | 500 | DATABASE_ERROR | Database operation failures |
| `VPNConfigError` | 400 | VPN_CONFIG_ERROR | VPN configuration issues |
| `OnboardingError` | 400 | ONBOARDING_ERROR | Onboarding process failures |
| `EmailExistsError` | 409 | EMAIL_EXISTS | Email already registered |
| `InvalidRequestError` | 400 | INVALID_REQUEST | Invalid request format |

#### Example Usage:
```python
from app.core.exceptions import CameraError, EmailExistsError

# Example 1: Camera connection error
raise CameraError(
    message="Camera IP/Port is not reachable",
    details={
        "ip": "192.168.1.100",
        "port": 8080,
        "reason": "Connection timeout"
    }
)

# Example 2: Email already exists
raise EmailExistsError(email="user@example.com")
```

---

### 2. **app/core/exception_handlers.py** (NEW)
Implements FastAPI exception handlers for proper HTTP response formatting.

#### Features:
- **Consistent Response Format**: All errors return a standardized JSON structure
- **Comprehensive Logging**: Every exception is logged with context
- **HTTP Status Mapping**: Proper HTTP status codes for each error type
- **Request Context**: Path and timestamp included in all error responses

#### Response Format:
```json
{
  "success": false,
  "timestamp": "2026-01-28T14:16:34.123456",
  "error": {
    "code": "CAMERA_ERROR",
    "message": "Camera IP/Port is not reachable",
    "details": {
      "ip": "192.168.1.100",
      "port": 8080,
      "reason": "Connection timeout"
    },
    "path": "/api/onboarding/onboarding_register/admin"
  }
}
```

#### Registered Handlers:
- `AppException` → Custom app exceptions
- `ValueError` → Validation errors (400)
- `RuntimeError` → Runtime errors (500)
- `Exception` → Generic exceptions (500)

---

### 3. **app/main.py** (UPDATED)
FastAPI application configuration with exception handlers registered.

```python
from app.core.exceptions import AppException
from app.core.exception_handlers import (
    app_exception_handler,
    general_exception_handler,
    value_error_handler,
    runtime_error_handler
)

# Register handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(ValueError, value_error_handler)
app.add_exception_handler(RuntimeError, runtime_error_handler)
app.add_exception_handler(Exception, general_exception_handler)
```

---

### 4. **app/service/admin/admin_regester.py** (UPDATED)
Updated with comprehensive exception handling and logging.

#### Key Changes:
✅ Replaced `HTTPException` with custom `EmailExistsError`
✅ Added logging at each step
✅ Proper error handling for database operations
✅ Detailed error responses with context
✅ Docstrings for all functions

#### Example Error Response:
```json
{
  "success": false,
  "timestamp": "2026-01-28T14:16:34.123456",
  "error": {
    "code": "EMAIL_EXISTS",
    "message": "Email already registered",
    "details": {
      "email": "user@example.com"
    },
    "path": "/api/users/register/admin"
  }
}
```

---

### 5. **app/service/admin/onboarding_regester.py** (UPDATED)
Updated with comprehensive exception handling, logging, and camera validation.

#### Key Changes:
✅ Enhanced `check_camera()` function with detailed error handling
✅ Added logging for each onboarding step
✅ Proper exception handling for camera, database, and general errors
✅ Detailed error responses with operation context
✅ Type hints for all parameters

#### Camera Validation Response (Success):
```json
{
  "success": true,
  "message": "Admin onboarding completed successfully",
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "tokenType": "Bearer",
  "user": {
    "id": 1,
    "organizationId": 1,
    "branchId": 1
  },
  "nextPage": "/dashboard"
}
```

#### Camera Validation Response (Failure):
```json
{
  "success": false,
  "timestamp": "2026-01-28T14:16:34.123456",
  "error": {
    "code": "CAMERA_ERROR",
    "message": "Camera IP/Port is not reachable",
    "details": {
      "ip": "192.168.1.100",
      "port": 8080,
      "reason": "IP/Port not reachable: [Errno 10061] No connection could be made..."
    },
    "path": "/api/onboarding/onboarding_register/admin"
  }
}
```

---

## Logging System

### Log Levels Used:
- **INFO**: Success operations, state changes
- **WARNING**: Non-critical issues, potential problems
- **ERROR**: Failures that need attention

### Example Log Messages:
```
2026-01-28 14:16:34,006 INFO Starting onboarding for user: 1
2026-01-28 14:16:34,007 INFO Validating camera: 192.168.1.100:8080
2026-01-28 14:16:34,100 ERROR Camera IP/Port unreachable: Connection timeout after 5s
2026-01-28 14:16:34,102 ERROR Application error during onboarding: Camera IP/Port is not reachable
```

---

## Usage Examples

### Example 1: Camera Connection Error
**Request:**
```bash
POST /api/onboarding/onboarding_register/admin
{
  "ip_address": "192.168.1.999",
  "port": 8080,
  ...
}
```

**Response (400 - Bad Request):**
```json
{
  "success": false,
  "timestamp": "2026-01-28T14:16:34.123456",
  "error": {
    "code": "CAMERA_ERROR",
    "message": "Camera IP/Port is not reachable",
    "details": {
      "ip": "192.168.1.999",
      "port": 8080,
      "reason": "IP/Port not reachable: [Errno 11001] getaddrinfo failed"
    },
    "path": "/api/onboarding/onboarding_register/admin"
  }
}
```

---

### Example 2: Email Already Exists
**Request:**
```bash
POST /api/users/register/admin
{
  "email": "existing@example.com",
  ...
}
```

**Response (409 - Conflict):**
```json
{
  "success": false,
  "timestamp": "2026-01-28T14:16:34.123456",
  "error": {
    "code": "EMAIL_EXISTS",
    "message": "Email already registered",
    "details": {
      "email": "existing@example.com"
    },
    "path": "/api/users/register/admin"
  }
}
```

---

### Example 3: Password Mismatch
**Request:**
```bash
POST /api/users/register/admin
{
  "password": "Password123!",
  "confirm_password": "DifferentPassword123!",
  ...
}
```

**Response (400 - Bad Request):**
```json
{
  "success": false,
  "timestamp": "2026-01-28T14:16:34.123456",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Password and confirm password do not match",
    "details": {},
    "path": "/api/users/register/admin"
  }
}
```

---

### Example 4: Database Error
**Response (500 - Internal Server Error):**
```json
{
  "success": false,
  "timestamp": "2026-01-28T14:16:34.123456",
  "error": {
    "code": "DATABASE_ERROR",
    "message": "Failed to save onboarding data",
    "details": {
      "operation": "onboarding_setup",
      "error": "IntegrityError: duplicate key value violates unique constraint..."
    },
    "path": "/api/onboarding/onboarding_register/admin"
  }
}
```

---

## Best Practices for Using This System

### 1. Always Import and Use Custom Exceptions
```python
from app.core.exceptions import CameraError, DatabaseError, ValidationError

# ✅ Good
raise CameraError(
    message="Camera connection failed",
    details={"ip": ip, "port": port}
)

# ❌ Bad
raise Exception("Camera connection failed")
```

### 2. Include Detailed Context
```python
# ✅ Good - provides actionable information
raise CameraError(
    message="Camera IP/Port is not reachable",
    details={
        "ip": request.ip_address,
        "port": request.port,
        "timeout": 5,
        "reason": str(socket_error)
    }
)

# ❌ Bad - vague error
raise CameraError(message="Camera error")
```

### 3. Log at Each Major Step
```python
logger.info(f"Starting operation for user: {user_id}")
logger.info(f"Step 1: Validating camera at {ip}:{port}")
logger.warning("Step 2: Camera stream not opening (continuing...)")
logger.error("Operation failed: {error_details}")
```

### 4. Handle Specific Exceptions First
```python
try:
    # operation code
except CameraError:
    # handle camera-specific error
    logger.error(f"Camera error: {e}")
    raise
except DatabaseError:
    # handle database-specific error
    logger.error(f"Database error: {e}")
    raise
except Exception as unexpected:
    # handle unexpected errors
    logger.error(f"Unexpected error: {e}")
    raise OnboardingError(...)
```

---

## Monitoring and Debugging

### View Logs in Terminal:
```bash
# All logs
tail -f app.log

# Only errors
grep "ERROR" app.log

# Specific service
grep "onboarding_regester" app.log
```

### Common Error Codes to Monitor:
- `CAMERA_ERROR` - Camera connectivity issues
- `DATABASE_ERROR` - Database operation failures
- `EMAIL_EXISTS` - Duplicate user registration attempts
- `VALIDATION_ERROR` - Invalid request data
- `INTERNAL_ERROR` - Unexpected system errors

---

## Testing the Exception System

### Test Case 1: Camera Connection Error
```bash
curl -X POST http://localhost:8000/api/onboarding/onboarding_register/admin \
  -H "Content-Type: application/json" \
  -d '{
    "ip_address": "invalid_ip",
    "port": 8080,
    ...
  }'
```

### Test Case 2: Email Duplicate
```bash
curl -X POST http://localhost:8000/api/users/register/admin \
  -H "Content-Type: application/json" \
  -d '{
    "email": "existing@example.com",
    ...
  }'
```

---

## Summary

✅ **Centralized Exception Handling** - All exceptions handled in one place
✅ **Consistent Response Format** - All errors follow the same structure
✅ **Comprehensive Logging** - Track application flow and errors
✅ **Proper HTTP Status Codes** - Clients get correct status codes
✅ **Detailed Error Context** - Error details help with debugging
✅ **Type Safety** - Custom exceptions with proper typing
✅ **Production Ready** - Suitable for production deployments

