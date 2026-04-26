from flask_restful import Resource
from app.services.analytics_service import AnalyticsService
from app.exceptions import DatabaseError


class CategoryWiseResource(Resource):
    def get(self):
        try:
            report = AnalyticsService.category_wise()
            return {
                       "Category_wise_report": report
                   }, 200
        except DatabaseError as e:
            print(e.__cause__)
            return {
                       "error": "Internal Server Error"
                   }, 500


class MonthlyReportResource(Resource):
    def get(self):
        try:
            report = AnalyticsService.monthly_report()
            return {
                       "monthly_wise_report": report
                   }, 200
        except DatabaseError as e:
            print(e.__cause__)
            return {
                       "message": "Internal Server Error"
                   }, 500


class SummaryResource(Resource):
    def get(self):
        try:
            summary = AnalyticsService.summary()
            return {
                       "summary": summary
                   }, 200
        except DatabaseError as e:
            print(e.__cause__)
            return {
                       "error": "Internal Server Error"
                   }, 500
