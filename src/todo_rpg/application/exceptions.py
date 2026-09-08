from todo_rpg.domain.exceptions import ToDoRpgBaseException


class UserNotFoundError(ToDoRpgBaseException):
    pass


class TaskNotFoundError(ToDoRpgBaseException):
    pass


class TaskNotFoundInHistoryError(ToDoRpgBaseException):
    pass


class TaskHistoryNotFoundError(ToDoRpgBaseException):
    pass


class SkillNotFoundError(ToDoRpgBaseException):
    pass


class ItemNotFoundError(ToDoRpgBaseException):
    pass


class SessionNotFoundError(ToDoRpgBaseException):
    pass


class AccessDeniedError(ToDoRpgBaseException):
    pass


class TaskCategoryNotFoundError(ToDoRpgBaseException):
    pass


class ShopListingNotFoundError(ToDoRpgBaseException):
    pass


class ShopTransactionNotFoundError(ToDoRpgBaseException):
    pass


class InventoryItemNotFoundError(ToDoRpgBaseException):
    pass


class ShopListingAlreadyExistsError(ToDoRpgBaseException):
    pass


class UserRankNotFoundError(ToDoRpgBaseException):
    pass
