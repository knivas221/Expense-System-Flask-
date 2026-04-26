from pymongo.errors import BulkWriteError, PyMongoError

from app import mongo_client
from app.utils.expense_helper import serialize_mongo_db


def get_db():
    if mongo_client is None:
        raise RuntimeError("MongoDB client not initialized. Did you call create_app()?")
    db = mongo_client.get_default_database()
    collection = db["expense"]
    collection.create_index("expense_id", unique=True)
    collection.create_index("expense_date")
    collection.create_index("category")
    return collection


class ExpenseRepo:

    @staticmethod
    def get_all_expenses(page=1, page_size=50):
        skip = (page - 1) * page_size
        collection = get_db()
        cursor = collection.find({}, {"_id": 0}).skip(skip).limit(page_size)
        expenses = [serialize_mongo_db(doc) for doc in cursor]
        return expenses

    @staticmethod
    def get_expense_id(expense_id):
        collection = get_db()
        result = collection.find_one({"expense_id": expense_id}, {"_id": 0})
        if result is None:
            return None
        expense = serialize_mongo_db(result)
        return expense

    @staticmethod
    def add_expense(expense):
        collection = get_db()
        already_exists = collection.find_one({"expense_id": expense.get("expense_id")}, {"_id": 0})
        if already_exists is not None:
            return None
        result = collection.insert_one(expense)
        return str(result.inserted_id)

    @staticmethod
    def update_expense_using_id(expense, expense_id):
        collection = get_db()
        already_exists = collection.find_one({"expense_id": expense_id}, {"_id": 0})
        if already_exists is None:
            return None
        result = collection.update_one({"expense_id": expense_id}, {"$set": expense})
        return result.modified_count

    @staticmethod
    def delete_expense_using_id(expense_id):
        collection = get_db()
        result = collection.delete_one({"expense_id": expense_id})
        return result.deleted_count

    @staticmethod
    def get_all_expenses_for_analytics():
        collection = get_db()
        cursor = collection.find({}, {"_id": 0})
        expenses_list = [serialize_mongo_db(expense) for expense in cursor]
        return expenses_list

    @staticmethod
    def add_expenses_bulk(expenses: list[dict]):
        """
        Pure DB operation.
        Inserts multiple documents using insert_many.
        Raises DB exceptions upward.
        """
        if not expenses:
            return []

        collection = get_db()

        try:
            result = collection.insert_many(expenses, ordered=False)
            return result.inserted_ids

        except (BulkWriteError, PyMongoError):
            # Do NOT handle here — service decides behavior
            raise
