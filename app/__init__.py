# app/__init__.py

from flask import Flask
from flask_restful import Api
from pymongo import MongoClient

mongo_client = None


def create_app():
    global mongo_client

    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Init REST API
    api = Api(app)

    # Init MongoDB (ONCE)
    mongo_client = MongoClient(app.config["MONGO_URI"])

    # Register resources
    from app.resources.expense_resource import ExpensesResource, ExpenseResource, AddExpenseResource, UpdateExpenseResource, DeleteExpenseResource
    from app.resources.analytics_resource import CategoryWiseResource, MonthlyReportResource, SummaryResource
    from app.resources.bulk_upload_resource import ExpenseBulkUploadResource

    api.add_resource(ExpensesResource, "/get_expenses")
    api.add_resource(ExpenseResource, "/get_expense")
    api.add_resource(AddExpenseResource, "/add_expense")
    api.add_resource(UpdateExpenseResource, "/update_expense")
    api.add_resource(DeleteExpenseResource, "/delete_expense")
    api.add_resource(CategoryWiseResource, "/category_wise")
    api.add_resource(MonthlyReportResource, "/monthly_wise")
    api.add_resource(SummaryResource, "/summary")
    api.add_resource(ExpenseBulkUploadResource, "/bulk_upload")

    return app
