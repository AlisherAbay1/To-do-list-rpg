class ToDoRpgBaseException(Exception):
    pass


class TaskAlreadyDoneError(ToDoRpgBaseException):
    pass


class TaskExecutedTooEarlyError(ToDoRpgBaseException):
    pass


class EmailAlreadyTakenError(ToDoRpgBaseException):
    pass


class IncorrectPasswordError(ToDoRpgBaseException):
    pass


class UsernameAlreadyTakenError(ToDoRpgBaseException):
    pass


class ShopListingAmountIsZeroError(ToDoRpgBaseException):
    pass


class UserBalanceNotEnoughError(ToDoRpgBaseException):
    pass


class UserDoesntFitSkillRequirementsError(ToDoRpgBaseException):
    pass


class SkillIsAlreadyInRequirementsError(ToDoRpgBaseException):
    pass
