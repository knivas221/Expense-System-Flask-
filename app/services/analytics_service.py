from app.repository.expense_repo import ExpenseRepo
from app.analytics.expense_analytics import ExpenseAnalytics
from pymongo.errors import PyMongoError
from app.exceptions import DatabaseError


class AnalyticsService:

    @staticmethod
    def category_wise():
        try:
            expenses_list = ExpenseRepo.get_all_expenses_for_analytics()
            report = ExpenseAnalytics.category_wise(expenses_list)
            return report
        except PyMongoError as e:
            raise DatabaseError("Failed to connect with database.") from e

    @staticmethod
    def monthly_report():
        try:
            expense_list = ExpenseRepo.get_all_expenses_for_analytics()
            report = ExpenseAnalytics.monthly(expense_list)
            return report
        except PyMongoError as e:
            raise DatabaseError("Failed to connect with database.") from e

    @staticmethod
    def summary():
        try:
            expense_list = ExpenseRepo.get_all_expenses_for_analytics()
            summary = ExpenseAnalytics.summary(expense_list)
            return summary
        except PyMongoError as e:
            raise DatabaseError("Failed to connect with database.") from e
