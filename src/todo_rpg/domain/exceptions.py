class TaskAlreadyDoneError(Exception):
    pass


class TaskExecutedTooEarlyError(Exception):
    pass


class EmailAlreadyTakenError(Exception):
    pass


class IncorrectPasswordError(Exception):
    pass


class UsernameAlreadyTakenError(Exception):
    pass


class ShopListingAmountIsZeroError(Exception):
    pass


class UserBalanceNotEnoughError(Exception):
    pass


class UserDoesntFitSkillRequirementsError(Exception):
    pass


class SkillIsAlreadyInRequirementsError(Exception):
    pass
