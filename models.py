from datetime import datetime

class Transaction:
    def __init__(self, amount, category, t_type, date=None, description=""):
        self.amount = amount
        self.category = category
        self.type = t_type  # "income" or "expense"
        self.date = date or datetime.now().strftime("%Y-%m-%d")
        self.description = description

    def to_dict(self):
        return self.__dict__
