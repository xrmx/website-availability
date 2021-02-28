class CheckerNetworkError(Exception):
    """Generic exception for network errors"""
    def __init__(self, original_exception):
        self.checker_original_exception = original_exception
