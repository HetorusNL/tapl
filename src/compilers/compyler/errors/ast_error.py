class AstError(BaseException):
    def __init__(self, message: str):
        super().__init__(message)
