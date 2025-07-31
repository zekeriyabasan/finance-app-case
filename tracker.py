import os
import pandas as pd
import datetime
import matplotlib.pyplot as plt

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



    def monthly_category_report(self, year):
        if not pd.api.types.is_datetime64_any_dtype(self.df["date"]):
            self.df["date"] = pd.to_datetime(self.df["date"], format="%Y-%m-%d %H:%M:%S", errors='coerce')

        self.df["amount"] = pd.to_numeric(self.df["amount"], errors="coerce")
        
        df_year = self.df[self.df["date"].dt.year == year].copy()
        df_year["month"] = df_year["date"].dt.month
        grouped = df_year.groupby(["month", "category"])["amount"].sum().unstack(fill_value=0)
        grouped = grouped.reindex(range(1, 13), fill_value=0)
        return grouped
    
    def draw_monthly_report_chart(self, year):
        data = self.monthly_category_report(year)
        print(data)
        ax = data.plot(kind="bar", stacked=False, figsize=(12,6))
        ax.set_title(f"{year} Yılı Aylık Kategori Bazlı Harcamalar")
        ax.set_xlabel("Ay")
        ax.set_ylabel("Toplam Tutar (₺)")
        ax.set_xticklabels([str(m) for m in range(1, 13)], rotation=0)
        plt.legend(title="Kategori")
        plt.show()

    def yearly_category_report(self):
        # Tarih kolonunu datetime yap, hatalı olanları NaT yap
        if not pd.api.types.is_datetime64_any_dtype(self.df["date"]):
            self.df["date"] = pd.to_datetime(self.df["date"], errors='coerce')
    
        # Geçersiz tarihleri içeren satırları çıkar
        df_clean = self.df.dropna(subset=["date"]).copy()
    
        # Amount değerlerini sayısala çevir, hatalıları NaN yap
        df_clean["amount"] = pd.to_numeric(df_clean["amount"], errors="coerce")
    
        # Amount NaN olanları da düşürmek isteyebilirsin
        df_clean = df_clean.dropna(subset=["amount"])
    
        # Yıl bazında gruplama
        grouped = df_clean.groupby([df_clean["date"].dt.year.rename("year"), "category"])["amount"]\
            .sum().unstack(fill_value=0)
    
        return grouped



    def draw_yearly_report_chart(self):
        data = self.yearly_category_report()
        print(data)  # istersen yazdırabilirsin

        ax = data.plot(kind="bar", stacked=False, figsize=(12,6))
        ax.set_title("Yıllık Kategori Bazlı Harcamalar")
        ax.set_xlabel("Yıl")
        ax.set_ylabel("Toplam Tutar (₺)")
        ax.legend(title="Kategori")
        plt.tight_layout()
        plt.show()


