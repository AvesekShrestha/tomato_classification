from fastapi import HTTPException

class AppException(HTTPException):
    def __init__(self, status_code: int, message: str):
        super().__init__(status_code=status_code, detail=message)


class BadRequest(AppException):
    def __init__(self, message: str = "Bad request"):
        super().__init__(status_code=400, message=message)


class Unauthorized(AppException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(status_code=401, message=message)


class Forbidden(AppException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(status_code=403, message=message)


class NotFound(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(status_code=404, message=message)


class Conflict(AppException):
    def __init__(self, message: str = "Conflict"):
        super().__init__(status_code=409, message=message)


class InternalServerError(AppException):
    def __init__(self, message: str = "Internal server error"):
        super().__init__(status_code=500, message=message)

class ValueError(AppException):
    def __init__(self, message: str = "Invalid Value"):
        super().__init__(status_code=400, message=message)

class TokenExpired(AppException):
    def __init__(self, message: str = "Token Expired"):
        super().__init__(status_code=400, message=message)

class OTPExpired(AppException):
    def __init__(self, message: str = "OTP Expired"):
        super().__init__(status_code=400, message=message)

