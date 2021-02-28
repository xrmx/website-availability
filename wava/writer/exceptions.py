class WriterError(Exception):
    """Generic exception for writer errors"""

    def __init__(self, original_exception):
        self.writer_original_exception = original_exception


class WriterConnectionError(Exception):
    """Exception for errors while connecting to the database"""

    def __init__(self, original_exception):
        self.writer_original_exception = original_exception
