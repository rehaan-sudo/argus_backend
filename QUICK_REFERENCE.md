# Quick Reference Guide - Exception Handling

## Copy-Paste Examples

### 1. Basic Exception with Details
```python
from app.core.exceptions import ValidationError

raise ValidationError(
    message="Invalid input format",
    details={
        "field": "email",
        "provided": "not-an-email",
        "required": "valid email format"
    }
)
```

**Response:**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input format",
    "details": {
      "field": "email",
      "provided": "not-an-email",
      "required": "valid email format"
    }
  }
}
```

---

### 2. Camera Error Example
```python
from app.core.exceptions import CameraError
import logging

logger = logging.getLogger(__name__)

try:
    # camera connection code
    sock = socket.create_connection((ip, port), timeout=5)
except Exception as e:
    logger.error(f"Camera connection failed: {str(e)}")
    raise CameraError(
        message="Cannot connect to camera",
        details={
            "ip": ip,
            "port": port,
            "error": str(e)
        }
    )
```

---

### 3. Database Error with Rollback
```python
from app.core.exceptions import DatabaseError
import logging

logger = logging.getLogger(__name__)

try:
    # database operations
    db.add(new_object)
    await db.flush()
    await db.commit()
except Exception as db_error:
    await db.rollback()
    logger.error(f"Database operation failed: {str(db_error)}")
    raise DatabaseError(
        message="Failed to save data to database",
        details={
            "operation": "user_creation",
            "error": str(db_error)
        }
    )
```

---

### 4. Email Duplicate Check
```python
from app.core.exceptions import EmailExistsError
import logging

logger = logging.getLogger(__name__)

result = await db.execute(
    select(User).where(User.email == request.email)
)
if result.scalar_one_or_none():
    logger.warning(f"Email already registered: {request.email}")
    raise EmailExistsError(request.email)
```

**Response:**
```json
{
  "success": false,
  "error": {
    "code": "EMAIL_EXISTS",
    "message": "Email already registered",
    "details": {
      "email": "user@example.com"
    }
  }
}
```

---

### 5. Logging Pattern
```python
import logging

logger = logging.getLogger(__name__)

# At the start
logger.info(f"Starting operation for user: {user_id}")

# During operation
logger.info(f"Created user with ID: {user.id}")
logger.warning(f"Camera stream not optimal: {warning_msg}")

# On error
logger.error(f"Operation failed: {error_details}")

# On success
logger.info(f"Operation completed successfully")
```

---

### 6. Try-Except Pattern
```python
from app.core.exceptions import (
    CameraError, 
    DatabaseError, 
    OnboardingError
)
import logging

logger = logging.getLogger(__name__)

try:
    logger.info("Starting onboarding process")
    
    # Step 1: Camera validation
    logger.info(f"Validating camera: {ip}:{port}")
    camera_result = check_camera(ip, port)
    if not camera_result["ip_status"]:
        raise CameraError(...)
    
    # Step 2: Database operations
    logger.info("Creating user records")
    await db.commit()
    
    logger.info("Onboarding completed successfully")
    return success_response
    
except (CameraError, DatabaseError) as app_error:
    logger.error(f"Application error: {str(app_error)}")
    raise app_error

except Exception as unexpected:
    logger.error(f"Unexpected error: {str(unexpected)}")
    raise OnboardingError(
        message="An unexpected error occurred",
        details={"error": str(unexpected)}
    )
```

---

### 7. Validation Error with Multiple Fields
```python
from app.core.exceptions import ValidationError

def validate_user_input(request):
    errors = {}
    
    if not request.email or "@" not in request.email:
        errors["email"] = "Invalid email format"
    
    if len(request.password) < 8:
        errors["password"] = "Password must be at least 8 characters"
    
    if request.password != request.confirm_password:
        errors["confirm_password"] = "Passwords do not match"
    
    if errors:
        raise ValidationError(
            message="Validation failed",
            details=errors
        )
```

**Response:**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": {
      "email": "Invalid email format",
      "password": "Password must be at least 8 characters",
      "confirm_password": "Passwords do not match"
    }
  }
}
```

---

### 8. Resource Not Found
```python
from app.core.exceptions import NotFoundError

user = await db.execute(
    select(User).where(User.id == user_id)
)
user = user.scalar_one_or_none()

if not user:
    raise NotFoundError(
        resource="User",
        details={"user_id": user_id}
    )
```

**Response:**
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "User not found",
    "details": {
      "user_id": 123
    }
  }
}
```

---

### 9. VPN Configuration Error
```python
from app.core.exceptions import VPNConfigError

try:
    vpn = VpnConfig(
        branch_id=branch.branch_id,
        username=request.vpn_user,
        password=hash_password(request.vpn_password),
        site=request.site,
        config_file_path=request.config_path,
        is_active=True
    )
    db.add(vpn)
    await db.flush()
except Exception as e:
    logger.error(f"VPN configuration failed: {str(e)}")
    raise VPNConfigError(
        message="Failed to configure VPN",
        details={
            "site": request.site,
            "error": str(e)
        }
    )
```

---

### 10. Complete Service Function Template
```python
from app.core.exceptions import (
    CameraError, 
    DatabaseError, 
    ValidationError,
    OnboardingError
)
import logging

logger = logging.getLogger(__name__)

async def service_function(request, db, current_user):
    """
    Service function with proper exception handling
    
    Args:
        request: Request data
        db: Database session
        current_user: Current user
    
    Returns:
        Success response
    
    Raises:
        CameraError: If camera fails
        DatabaseError: If DB fails
        ValidationError: If validation fails
    """
    try:
        logger.info(f"Starting function for user: {current_user.id}")
        
        # Validation step
        logger.info("Validating input")
        if not request.valid_field:
            raise ValidationError("Invalid input")
        
        # Processing step
        logger.info("Processing data")
        try:
            # Database operations
            db.add(new_object)
            await db.flush()
            await db.commit()
            logger.info("Data saved successfully")
        except Exception as db_error:
            await db.rollback()
            logger.error(f"Database error: {str(db_error)}")
            raise DatabaseError("Failed to save data")
        
        # Success
        logger.info("Function completed successfully")
        return {
            "success": True,
            "message": "Operation completed",
            "data": result
        }
    
    except (CameraError, DatabaseError, ValidationError) as app_error:
        logger.error(f"Expected error: {str(app_error)}")
        raise app_error
    
    except Exception as unexpected:
        logger.error(f"Unexpected error: {str(unexpected)}")
        raise OnboardingError(
            message="An unexpected error occurred",
            details={"error": str(unexpected)}
        )
```

---

## Quick Decision Tree

```
Is it a validation error?
  → Use ValidationError

Is it a camera issue?
  → Use CameraError

Is it a database issue?
  → Use DatabaseError

Is it about authentication?
  → Use AuthenticationError

Is it about permissions?
  → Use AuthorizationError

Is it about missing resource?
  → Use NotFoundError

Is it about duplicate data?
  → Use ConflictError (or EmailExistsError for emails)

Is it about VPN config?
  → Use VPNConfigError

Is it about onboarding?
  → Use OnboardingError

Otherwise?
  → Use InvalidRequestError
```

---

## HTTP Status Code Quick Reference

| Status | Use Case | Exception |
|---|---|---|
| 400 | Bad request, validation failed | ValidationError |
| 401 | Not authenticated | AuthenticationError |
| 403 | Not authorized | AuthorizationError |
| 404 | Resource not found | NotFoundError |
| 409 | Conflict, duplicate entry | ConflictError |
| 500 | Server error, database error | DatabaseError |

---

## Common Patterns

### Pattern 1: Simple Success
```python
return {
    "success": True,
    "message": "Operation successful"
}
```

### Pattern 2: Success with Data
```python
return {
    "success": True,
    "message": "User created",
    "data": {
        "id": user.id,
        "email": user.email
    }
}
```

### Pattern 3: Success with Token
```python
return {
    "success": True,
    "message": "Login successful",
    "access_token": token,
    "tokenType": "Bearer"
}
```

### Pattern 4: Success with Multiple Fields
```python
return {
    "success": True,
    "message": "Onboarding completed",
    "access_token": token,
    "tokenType": "Bearer",
    "user": {
        "id": user.id,
        "organizationId": org.id
    },
    "nextPage": "/dashboard"
}
```

---

## Testing Each Exception Type

```bash
# Test ValidationError
curl -X POST http://localhost:8000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"email": "invalid", "password": "123"}'

# Test EmailExistsError
curl -X POST http://localhost:8000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"email": "existing@test.com", "password": "ValidPass123"}'

# Test CameraError
curl -X POST http://localhost:8000/api/onboarding \
  -H "Content-Type: application/json" \
  -d '{"ip_address": "999.999.999.999", "port": 8080}'

# Test DatabaseError
# (Usually happens during operations, hard to manually trigger)
```

---

## Remember

✅ Always log at important steps
✅ Always include context in error details
✅ Always rollback on database errors
✅ Always catch specific exceptions first
✅ Always provide meaningful error messages
✅ Always test your error handling
✅ Always check logs for issues
