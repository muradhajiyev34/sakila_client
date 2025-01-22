class DataBaseConnectionError(Exception):
    def __init__(self, msg: str = "Databese is not connected!"):
        super().__init__(msg)