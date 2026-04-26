from flask_restful import Resource
from flask import request
from app.services.expense_service import ExpenseService
from app.utils.expense_helper import validate_expense_date
from app.exceptions import InvalidPaginationError, DatabaseError, InvalidExpenseId, ExpenseAlreadyExists, \
    ExpenseNotFoundError


class ExpensesResource(Resource):

    def get(self):
        try:
            page = request.args.get("page")
            page_size = request.args.get("page_size")
            if not page or not page_size:
                return {
                    "Error": "Page or Page size is missing"
                }, 400
            expenses_list = ExpenseService.get_expenses(int(page), int(page_size))
            return {
                       "Expenses": expenses_list
                   }, 200

        except ValueError:
            return {
                       "Error": "Page and Page size must be integers..."
                   }, 400
        except InvalidPaginationError as e:
            return {
                       "Error": str(e)
                   }, 400
        except DatabaseError as e:
            print("original cause", e.__cause__)
            return {
                       "Error": "Internal Server Error"
                   }, 500


class ExpenseResource(Resource):

    def get(self):
        try:
            expense_id = request.args.get("expense_id")
            if not expense_id:
                return {
                    "message": "Please enter expense id...It is blank..."
                }, 400
            expense = ExpenseService.get_expense(expense_id)
            return {
                       "Expense": expense
                   }, 200

        except InvalidExpenseId as e:
            return {
                       "Error": str(e)
                   }, 404

        except DatabaseError as e:
            print("Error caused due: ", e.__cause__)
            return {
                       "Error": "Internal Server Error"
                   }, 500


class AddExpenseResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return {
                           "Error": "Request body must be JSON"
                       }, 400
            data["expense_date"] = validate_expense_date(data.get("expense_date"))
            required_fields = ["expense_id", "title", "amount", "category", "payment_method", "expense_date"]
            missing_fields = [field for field in required_fields if field not in data or data[field] in ("", None)]
            if missing_fields:
                return {
                           "Error": "Missing required Fields",
                           "Missing Fields": missing_fields
                       }, 400
            inserted_id = ExpenseService.add_expense(data)
            return {
                       "message": "Expense added successfully",
                       "InsertId": inserted_id
                   }, 201
        except ValueError as e:
            return {
                "Error": str(e)
            }, 400

        except ExpenseAlreadyExists as e:
            return {
                       "Error": str(e)
                   }, 409
        except DatabaseError as e:
            print("Error caused due: ", e.__cause__)
            return {
                       "Error": "Internal Server Error"
                   }, 500


class UpdateExpenseResource(Resource):
    def put(self):
        try:
            data = request.get_json()
            expense_id = request.args.get("expense_id")
            if not data:
                return {
                           "Error": "Request body must be Json"
                       }, 400

            if not expense_id:
                return {
                           "Error": "Expense_id is missing. Please enter the expense_id..."
                       }, 400

            if "expense_id" in data:
                return {
                           "Error": "Expense_id must not be in body..because we can't updated the id.."
                       }, 400
            required_fields = ["title", "amount", "category", "payment_method", "expense_date",
                               "created_at"]
            unknown_fields = [key for key in data.keys() if key not in required_fields]
            if unknown_fields:
                return {
                           "Error": "Found Unknown Fields, please enter allowed fields",
                           "UnknownFields": unknown_fields,
                           "AllowedFields": required_fields
                       }, 400
            result = ExpenseService.update_expense(data, expense_id)
            return {
                       "Message": "Updated the expense successfully",
                       "UpdatedStatus": result
                   }, 200

        except ExpenseNotFoundError as e:
            return {
                       "Error": str(e)
                   }, 404

        except DatabaseError as e:
            print(e.__cause__)
            return {
                       "Error": "Internal Server Error"
                   }, 500


class DeleteExpenseResource(Resource):

    def delete(self):
        try:
            expense_id = request.args.get("expense_id")
            if not expense_id:
                return {
                           "Error": "Expense_id is missing..Please enter it."
                       }, 400
            result = ExpenseService.delete_expense(expense_id)

            return {
                       "Message": "Expense is deleted successfully..",
                       "DeletedStatus": result
                   }, 200

        except ExpenseNotFoundError as e:
            return {
                       "Error": str(e)
                   }, 404

        except DatabaseError as e:
            print(e.__cause__)
            return {
                "Error": "Internal Server error"
            }, 500
