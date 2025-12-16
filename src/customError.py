class NotFoundError(Exception):
    message: str
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class RemainingProductCountChangeError(Exception):
    newCount: int
    def __init__(self, newCount: int):
        super().__init__(newCount)
        self.newCount = newCount
