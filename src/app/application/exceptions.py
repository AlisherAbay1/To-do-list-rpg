class UserNotFoundError(Exception):
    pass

class EmailAlreadyTakenError(Exception):
    pass

class IncorrectPasswordError(Exception):
    pass

class TaskNotFoundError(Exception):
    pass

class TaskNotFoundInHistoryError(Exception):
    pass

class TaskAlreadyDoneError(Exception):
    pass

class TaskExecutedTooEarlyError(Exception):
    pass

class SkillNotFoundError(Exception):
    pass

class ItemNotFoundError(Exception):
    pass

class UsernameAlreadyTakenError(Exception):
    pass

class SessionNotFoundError(Exception):
    pass

class AccessDeniedError(Exception):
    pass

class TaskCategoryNotFoundError(Exception):
    pass

class ShopListingNotFoundError(Exception):
    pass

class InventoryItemNotFoundError(Exception):
    pass