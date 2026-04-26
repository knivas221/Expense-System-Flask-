class AppError(Exception):
    """Base application exception"""
    pass


class DatabaseError(AppError):
    pass


class InvalidPaginationError(AppError):
    pass


class ExpenseNotFoundError(AppError):
    pass


class InvalidExpenseId(AppError):
    pass


class ExpenseAlreadyExists(AppError):
    pass
