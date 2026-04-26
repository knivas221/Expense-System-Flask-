class Expense:

    def __init__(self, expense_id, title, amount, category, payment_method, expense_date, created_at):
        self.expense_id = expense_id
        self.title = title
        self.amount = amount
        self.category = category
        self.payment_method = payment_method
        self.expense_date = expense_date
        self.created_at = created_at

    def validate_amount(self):
        if self.amount <= 0:
            raise ValueError("Amount must be greater than zero...")

    def to_dict(self):
        return {
            "expense_id": self.expense_id,
            "title": self.title,
            "amount": self.amount,
            "category": self.category,
            "payment_method": self.payment_method,
            "expense_date": self.expense_date,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["expense_id"],
            data["title"],
            data["amount"],
            data["category"],
            data["payment_method"],
            data["expense_date"],
            data["created_at"]
        )
