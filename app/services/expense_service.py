from app.repository.expense_repo import ExpenseRepo
from app.exceptions import InvalidPaginationError, DatabaseError, InvalidExpenseId, ExpenseAlreadyExists, \
    ExpenseNotFoundError
from pymongo.errors import PyMongoError
from app.models.expense import Expense
from datetime import datetime


class ExpenseService:
    @staticmethod
    def get_expenses(page=1, page_size=50):
        if page <= 0 or page_size <= 0:
            raise InvalidPaginationError(
                "Page or Page size must be greater than zero."
            )
        try:
            expenses_list = ExpenseRepo.get_all_expenses(page, page_size)
            return expenses_list

        except PyMongoError as e:
            raise DatabaseError("Failed to fetch expenses due.") from e

    @staticmethod
    def get_expense(expense_id):
        try:
            expense = ExpenseRepo.get_expense_id(expense_id)
            if expense is None:
                raise InvalidExpenseId("Invalid Expense Id...Please enter correct id..")
            return expense

        except PyMongoError as e:
            raise DatabaseError("Failed to fetch expense due: ") from e

    @staticmethod
    def add_expense(expense):
        try:
            expense["created_at"] = datetime.utcnow()
            expense_obj = Expense.from_dict(expense)
            expense_obj.validate_amount()
            inserted_id = ExpenseRepo.add_expense(expense_obj.to_dict())
            if inserted_id is None:
                raise ExpenseAlreadyExists("Expense_Id already exists..Enter different id..")
            return inserted_id

        except PyMongoError as e:
            raise DatabaseError("Failed to fetch expense due.") from e

    @staticmethod
    def update_expense(expense, expense_id):
        try:
            result = ExpenseRepo.update_expense_using_id(expense, expense_id)
            if result is None:
                raise ExpenseNotFoundError("Expense not found, Please enter the correct expense_id..")
            return True

        except PyMongoError as e:
            raise DatabaseError("Failed to connect with database.") from e

    @staticmethod
    def delete_expense(expense_id):
        try:
            result = ExpenseRepo.delete_expense_using_id(expense_id)
            if not result:
                raise ExpenseNotFoundError("Expense not found, Please enter the correct expense_id..")
            return True

        except PyMongoError as e:
            raise DatabaseError("Failed to connect with database.") from e
