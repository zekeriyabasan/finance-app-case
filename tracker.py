import os
import pandas as pd
import datetime

class FinanceTracker:
    def __init__(self, filename='storage.csv'):
        self.filename = filename
        if not os.path.exists(filename) or os.stat(filename).st_size == 0:
            self.df = pd.DataFrame(columns=["date", "type", "category", "amount", "note"])
            self.save()
        else:
            self.df = pd.read_csv(filename, parse_dates=["date"])

    def save(self):
        self.df.to_csv(self.filename, index=False)

    def add_record(self, record_type, category, amount, note=""):
        new_record = {
            "date": datetime.datetime.now(),
            "type": record_type,
            "category": category,
            "amount": float(amount),
            "note": note
        }
        self.df = pd.concat([self.df, pd.DataFrame([new_record])], ignore_index=True)
        self.save()

    def delete_record(self, index):
        self.df.drop(index=index, inplace=True)
        self.df.reset_index(drop=True, inplace=True)
        self.save()

    def edit_record(self, index, **kwargs):
        for key, value in kwargs.items():
            if key in self.df.columns:
                self.df.at[index, key] = value
        self.save()

    def report_by_category(self):
        return self.df.groupby(["type", "category"])["amount"].sum()

    def report_by_month(self):
        self.df['month'] = self.df['date'].dt.to_period('M')
        return self.df.groupby(['month', 'type'])['amount'].sum()

    def import_csv(self, path):
        imported = pd.read_csv(path, parse_dates=["date"])
        self.df = pd.concat([self.df, imported], ignore_index=True)
        self.save()

    def export_csv(self, export_path):
        self.df.to_csv(export_path, index=False)

    def spending_by_category(self):
        giderler = self.df[self.df["type"] == "gider"]
        return giderler.groupby("category")["amount"].sum().sort_values(ascending=False)
    
    def monthly_report(self):
        self.df["month"] = self.df["date"].dt.to_period("M")
        return self.df.groupby(["month", "type"])["amount"].sum().unstack(fill_value=0)
    
    def yearly_report(self):
        self.df["year"] = self.df["date"].dt.year
        return self.df.groupby(["year", "type"])["amount"].sum().unstack(fill_value=0)

