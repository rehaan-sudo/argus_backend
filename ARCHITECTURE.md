# Exception Handling System Architecture

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Request                             │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │  Route Handler/Service │
                    └────────────┬───────────┘
                                 │
                    ┌────────────▼────────────────┐
                    │   Exception Raised?        │
                    └────────────┬────────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        NO                       YES                      NO
        │                        │                        │
        ▼                        ▼                        ▼
    Continue           Is it AppException?          Is it ValueError?
                              │                        │
                        YES   │   NO                YES │
                        ▼     │   ▼                  ▼  │
                    ┌────────────────────────────────────┐
                    │  Exception Handler Matches?        │
                    └────────────┬───────────────────────┘
                                 │
                    ┌────────────▼───────────┐
                    │  Format Error Response │
                    └────────────┬───────────┘
                                 │
                    ┌────────────▼───────────┐
                    │  Log Exception         │
                    │  (with context)        │
                    └────────────┬───────────┘
                                 │
                    ┌────────────▼───────────────────┐
                    │  Return JSON Response          │
                    │  + HTTP Status Code            │
                    │  + Timestamp                   │
                    │  + Error Details               │
                    │  + Request Path                │
                    └────────────┬───────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │   FastAPI Response     │
                    └────────────────────────┘
```

---

## File Structure

```
argus_backend/
│
├── app/
│   ├── main.py                          ← Exception handlers registered here
│   │
│   ├── core/
│   │   ├── exceptions.py               ← Custom exception classes (NEW)
│   │   ├── exception_handlers.py       ← Exception handler logic (NEW)
│   │   ├── database.py
│   │   ├── auth/
│   │   └── ...
│   │
│   ├── service/
│   │   ├── admin/
│   │   │   ├── admin_regester.py       ← Updated with exception handling
│   │   │   └── onboarding_regester.py  ← Updated with exception handling
│   │   └── ...
│   │
│   └── ...
│
├── EXCEPTION_HANDLING.md                 ← Full documentation (NEW)
├── IMPLEMENTATION_SUMMARY.md             ← Summary (NEW)
├── QUICK_REFERENCE.md                    ← Quick guide (NEW)
│
└── requirement.txt
```

---

## Exception Hierarchy

```
Exception (Python built-in)
│
├─► ValueError ──────────┐
├─► RuntimeError ────────┤
└─► General Exception ───┤
                          │
                          └─► Generic Exception Handler (500)
                                    │
                                    ▼
                          Logged + JSON Response

Exception (Python built-in)
│
└─► AppException ◄─── All custom exceptions
    │
    ├─► ValidationError
    │   └─ HTTP 400 VALIDATION_ERROR
    │
    ├─► AuthenticationError
    │   └─ HTTP 401 AUTHENTICATION_ERROR
    │
    ├─► AuthorizationError
    │   └─ HTTP 403 AUTHORIZATION_ERROR
    │
    ├─► NotFoundError
    │   └─ HTTP 404 NOT_FOUND
    │
    ├─► ConflictError
    │   └─ HTTP 409 CONFLICT
    │
    ├─► CameraError
    │   └─ HTTP 400 CAMERA_ERROR
    │
    ├─► DatabaseError
    │   └─ HTTP 500 DATABASE_ERROR
    │
    ├─► VPNConfigError
    │   └─ HTTP 400 VPN_CONFIG_ERROR
    │
    ├─► OnboardingError
    │   └─ HTTP 400 ONBOARDING_ERROR
    │
    ├─► EmailExistsError
    │   └─ HTTP 409 EMAIL_EXISTS
    │
    └─► InvalidRequestError
        └─ HTTP 400 INVALID_REQUEST

    All share common features:
    - Standardized JSON response
    - Logging with context
    - HTTP status code
    - Error code identifier
    - Detailed error information
```

---

## Request-Response Lifecycle

### Successful Request
```
┌─────────────────────────────────────────────────────────────┐
│ 1. CLIENT REQUEST                                            │
│    POST /api/users/register/admin                           │
│    {                                                        │
│      "email": "newuser@example.com",                       │
│      "password": "SecurePass123!",                         │
│      "confirm_password": "SecurePass123!",                │
│      ...                                                   │
│    }                                                        │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. SERVICE PROCESSING                                        │
│    logger.info("Starting admin registration...")            │
│    logger.info("Checking email existence...")               │
│    logger.info("Creating admin user...")                    │
│    logger.info("Admin registered successfully")             │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. SUCCESS RESPONSE (200 OK)                               │
│    {                                                        │
│      "success": true,                                       │
│      "message": "Admin registered successfully",            │
│      "accessToken": "eyJhbGciOiJIUzI1NiIs...",            │
│      "tokenType": "Bearer",                                │
│      "user": {                                             │
│        "id": 1,                                            │
│        "name": "New User",                                 │
│        "email": "newuser@example.com",                     │
│        "role": "SUPER_ADMIN"                               │
│      }                                                     │
│    }                                                        │
└─────────────────────────────────────────────────────────────┘
```

### Failed Request - Email Already Exists
```
┌─────────────────────────────────────────────────────────────┐
│ 1. CLIENT REQUEST                                            │
│    POST /api/users/register/admin                           │
│    {                                                        │
│      "email": "existing@example.com",  ◄─── Already exists │
│      ...                                                   │
│    }                                                        │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. SERVICE PROCESSING                                        │
│    logger.info("Starting admin registration...")            │
│    logger.info("Checking email existence...")               │
│    logger.warning("Email already registered: ...")          │
│    RAISE EmailExistsError(email)                            │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. EXCEPTION CAUGHT                                          │
│    app_exception_handler triggered                          │
│    logger.error("Application error during...")              │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. ERROR RESPONSE (409 CONFLICT)                            │
│    {                                                        │
│      "success": false,                                      │
│      "timestamp": "2026-01-28T14:16:34.123456",           │
│      "error": {                                            │
│        "code": "EMAIL_EXISTS",                             │
│        "message": "Email already registered",              │
│        "details": {                                        │
│          "email": "existing@example.com"                   │
│        },                                                  │
│        "path": "/api/users/register/admin"                │
│      }                                                     │
│    }                                                        │
└─────────────────────────────────────────────────────────────┘
```

### Failed Request - Camera Connection
```
┌─────────────────────────────────────────────────────────────┐
│ 1. CLIENT REQUEST                                            │
│    POST /api/onboarding/onboarding_register/admin           │
│    {                                                        │
│      "ip_address": "192.168.1.999",                        │
│      "port": 8080,                                         │
│      ...                                                   │
│    }                                                        │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. SERVICE PROCESSING                                        │
│    logger.info("Starting onboarding...")                    │
│    logger.info("Validating camera...")                      │
│    check_camera(ip, port)  ◄─── Fails to connect           │
│    logger.error("Camera IP/Port unreachable...")            │
│    RAISE CameraError(...)                                   │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. EXCEPTION CAUGHT                                          │
│    app_exception_handler triggered                          │
│    logger.error("Application error during...")              │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. ERROR RESPONSE (400 BAD REQUEST)                         │
│    {                                                        │
│      "success": false,                                      │
│      "timestamp": "2026-01-28T14:16:34.123456",           │
│      "error": {                                            │
│        "code": "CAMERA_ERROR",                             │
│        "message": "Camera IP/Port is not reachable",       │
│        "details": {                                        │
│          "ip": "192.168.1.999",                            │
│          "port": 8080,                                     │
│          "reason": "[Errno 11001] getaddrinfo failed"     │
│        },                                                  │
│        "path": "/api/onboarding/onboarding_register/admin"│
│      }                                                     │
│    }                                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow for Each Step

### Step 1: Request Arrives
```
HTTP Request
    │
    └─► FastAPI Route
         │
         └─► Service Function
```

### Step 2: Validation
```
Service Function
    │
    ├─► Validate Input
    │    ├─ Success? → Continue
    │    └─ Failure? → Raise ValidationError
    │
    ├─► Check Email
    │    ├─ Not exists? → Continue
    │    └─ Exists? → Raise EmailExistsError
    │
    └─► Check Other Conditions
         ├─ OK? → Continue
         └─ Issue? → Raise Appropriate Exception
```

### Step 3: Processing
```
Processing
    │
    ├─► Database Operations
    │    ├─ Success? → Flush/Commit
    │    └─ Failure? → Rollback + Raise DatabaseError
    │
    └─► Other Operations
         ├─ Success? → Continue
         └─ Failure? → Raise Specific Exception
```

### Step 4: Response
```
Result
    │
    ├─► Success
    │    └─► Return Success Response
    │
    └─► Exception
         │
         ├─► Is it AppException?
         │    └─► app_exception_handler
         │         └─► Format error response + Log
         │
         ├─► Is it ValueError?
         │    └─► value_error_handler
         │         └─► Format error response (400) + Log
         │
         ├─► Is it RuntimeError?
         │    └─► runtime_error_handler
         │         └─► Format error response (500) + Log
         │
         └─► Is it Generic Exception?
              └─► general_exception_handler
                   └─► Format error response (500) + Log

All handlers:
    └─► Return JSON Response + Status Code
```

---

## Error Code to Status Code Mapping

```
ERROR CODE              →  HTTP STATUS  →  MEANING
─────────────────────────────────────────────────────
VALIDATION_ERROR        →  400          →  Bad Request
AUTHENTICATION_ERROR    →  401          →  Unauthorized
AUTHORIZATION_ERROR     →  403          →  Forbidden
NOT_FOUND              →  404          →  Not Found
CONFLICT               →  409          →  Conflict
EMAIL_EXISTS           →  409          →  Conflict
CAMERA_ERROR           →  400          →  Bad Request
VPN_CONFIG_ERROR       →  400          →  Bad Request
ONBOARDING_ERROR       →  400          →  Bad Request
INVALID_REQUEST        →  400          →  Bad Request
DATABASE_ERROR         →  500          →  Server Error
INTERNAL_ERROR         →  500          →  Server Error
```

---

## Logging Flow

```
Application Start
    │
    ▼
Logger Configured
    │
    ├─► INFO: Normal operations
    │    └─ Example: "Starting admin registration for email: user@example.com"
    │
    ├─► WARNING: Potential issues
    │    └─ Example: "Email already registered: existing@example.com"
    │
    └─► ERROR: Failures
         └─ Example: "Camera IP/Port unreachable: Connection timeout"

All logs include:
    ├─ Timestamp
    ├─ Level (INFO/WARNING/ERROR)
    ├─ Module name
    ├─ Message with context
    └─ Stack trace (for errors)
```

---

## Integration Points

```
┌──────────────────────────────────────┐
│         Client Application           │
└────────────────┬─────────────────────┘
                 │
┌────────────────▼──────────────────────┐
│         FastAPI Application           │
│  (main.py with exception handlers)    │
└────────────────┬──────────────────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
    ▼            ▼            ▼
┌────────┐  ┌────────┐  ┌──────────┐
│ Routes │  │ Schemas│  │ Services │
└────┬───┘  └────────┘  └────┬─────┘
     │                       │
     └───────────┬───────────┘
                 │
    ┌────────────▼─────────────┐
    │ Exception Handling Layer  │
    │ (exceptions.py)           │
    │ (exception_handlers.py)   │
    └────────────┬──────────────┘
                 │
    ┌────────────▼──────────────┐
    │     Database Layer        │
    │     (models, schemas)     │
    └───────────────────────────┘

┌──────────────────────────────────────┐
│         Logging System               │
│  (captures all operations & errors)  │
└──────────────────────────────────────┘
```

---

## Performance Considerations

```
Exception Handling Overhead
    │
    ├─► Creating Exception Object
    │    ├─ Minimal overhead
    │    └─ Only when error occurs
    │
    ├─► Logging
    │    ├─ File I/O for logs
    │    └─ Negligible for most cases
    │
    ├─► JSON Serialization
    │    ├─ Fast conversion to JSON
    │    └─ Standard Python operation
    │
    └─► Database Rollback
         ├─ Only on error
         ├─ Cleans up partial changes
         └─ Important for data integrity

Normal Path (No Errors):
    └─ Zero exception handling overhead
      └─ Optimal performance
```

---

## Summary

The exception handling system provides:
- ✅ Centralized error management
- ✅ Consistent response format
- ✅ Comprehensive logging
- ✅ Proper HTTP status codes
- ✅ Detailed error context
- ✅ Production-ready solution
