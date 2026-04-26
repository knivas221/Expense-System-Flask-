import pandas as pd
from datetime import datetime
from pymongo.errors import BulkWriteError, PyMongoError

from app.models.expense import Expense
from app.repository.expense_repo import ExpenseRepo
from app.utils.expense_helper import validate_expense_date
from app.exceptions import DatabaseError


class BulkUploadService:

    @staticmethod
    def upload_expenses(file):
        df = pd.read_csv(file)

        valid_expenses = []
        rejected_rows = []

        for index, row in df.iterrows():
            try:
                expense_data = row.to_dict()

                # Validate & normalize fields
                expense_data["expense_date"] = validate_expense_date(
                    expense_data.get("expense_date")
                )
                expense_data["created_at"] = datetime.utcnow()

                # Domain model
                expense = Expense.from_dict(expense_data)
                expense.validate_amount()

                valid_expenses.append(expense.to_dict())

            except Exception as e:
                rejected_rows.append({
                    "row": index + 1,
                    "expense_id": row.get("expense_id"),
                    "error": str(e)
                })

        try:
            inserted_ids = ExpenseRepo.add_expenses_bulk(valid_expenses)

            return {
                "total_rows": len(df),
                "valid_rows": len(valid_expenses),
                "inserted": len(inserted_ids),
                "failed": len(rejected_rows),
                "rejected_rows": rejected_rows
            }

        except BulkWriteError as e:
            # Partial success handled here
            return {
                "total_rows": len(df),
                "valid_rows": len(valid_expenses),
                "inserted": e.details.get("nInserted", 0),
                "failed": len(rejected_rows) + len(e.details.get("writeErrors", [])),
                "db_errors": e.details.get("writeErrors", []),
                "rejected_rows": rejected_rows
            }

        except PyMongoError as e:
            raise DatabaseError("Bulk expense insert failed.") from e
