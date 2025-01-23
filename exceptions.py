class DataBaseConnectionError(Exception):
    """
    Custom exception class to handle database connection errors.
    Inherits from the base Exception class.
    """

    def __init__(self, msg: str = "Databese is not connected!"):
        """
        Initializes the DataBaseConnectionError with an optional error message.
        
        Parameters:
        - msg (str): A descriptive error message. Defaults to "Databese is not connected!".
        
        The message is passed to the parent Exception class.
        """
        super().__init__(msg)
