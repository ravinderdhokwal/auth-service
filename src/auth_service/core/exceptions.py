class AppException(Exception):
    def __init__(self, message: str, status_code: int = 400, data: dict | list | None = None):
        self.message = message
        self.status_code = status_code
        self.data = data

class NotFoundError(AppException):
    def __init__(self, message: str, status_code: int = 404):
        super().__init__(message, status_code)

class UnauthorizedError(AppException):
    def __init__(self, message: str = "Unauthorized.", status_code: int = 401):
        super().__init__(message, status_code)
