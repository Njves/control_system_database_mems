class NotFoundException(Exception):
    """
    An exception called when something was not found
    """

    def __int__(self):
        super().__init__("Couldn't find something")


class AccountNotFoundException(Exception):
    """
    An exception called when account was not found in any storage
    """

    def __init__(self):
        super().__init__("Account has not found")