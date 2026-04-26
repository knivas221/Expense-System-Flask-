import pandas as pd


class ExpenseAnalytics:

    @staticmethod
    def _prepare_dataframe(expenses):
        if not expenses:
            return pd.DataFrame()

        df = pd.DataFrame(expenses)
        df["amount"] = df["amount"].astype(float)
        df["expense_date"] = pd.to_datetime(df["expense_date"], errors="coerce")
        return df

    @staticmethod
    def category_wise(expenses):
        df = ExpenseAnalytics._prepare_dataframe(expenses)
        if df.empty:
            return []
        result = df.groupby("category")["amount"].sum().reset_index().sort_values(by="amount", ascending=False)
        return result.to_dict(orient="records")

    @staticmethod
    def monthly(expenses):
        df = ExpenseAnalytics._prepare_dataframe(expenses)
        if df.empty:
            return []
        df["month"] = df["expense_date"].dt.to_period("M").astype(str)
        result = df.groupby("month")["amount"].sum().reset_index().sort_values(by="month")
        return result.to_dict(orient="records")

    @staticmethod
    def summary(expenses):
        df = ExpenseAnalytics._prepare_dataframe(expenses)
        if df.empty:
            return []
        total_expenses = df["amount"].sum()
        df["month"] = df["expense_date"].dt.to_period("M").astype(str)
        monthly_totals = df.groupby("month")["amount"].sum()
        highest_spending_month = monthly_totals.idxmax()
        category_totals = df.groupby("category")["amount"].sum()
        highest_category = category_totals.idxmax()
        return {
            "total_expense": total_expenses,
            "highest_spending_month": highest_spending_month,
            "top_category": highest_category
        }
