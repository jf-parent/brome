
class InitDriverException(Exception):
    """Raise when the driver failed initializing
    Args:
        msg (str): Human readable string describing the exception.
    """

    def __init__(self, msg):
        self.msg = msg
