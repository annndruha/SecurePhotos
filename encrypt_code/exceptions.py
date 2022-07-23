class ExtensionError(Exception):
    def __init__(self, message="Extension doesn't support."):
        super().__init__(message)
