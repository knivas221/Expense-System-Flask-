from flask_restful import Resource
from flask import request

from app.services.bulk_upload_service import BulkUploadService
from app.exceptions import DatabaseError


class ExpenseBulkUploadResource(Resource):

    def post(self):
        if "file" not in request.files:
            return {"Error": "CSV file is required"}, 400

        file = request.files["file"]

        if not file.filename.endswith(".csv"):
            return {"Error": "Only CSV files are allowed"}, 400

        try:
            result = BulkUploadService.upload_expenses(file)
            return result, 201

        except DatabaseError:
            return {"Error": "Internal Server Error"}, 500
