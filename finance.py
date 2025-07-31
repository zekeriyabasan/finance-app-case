import pandas as pd
import matplotlib.pyplot as plt

class FinanceTracker:
    def __init__(self, df):
        self.df = df
    
    def monthly_category_report(self, year):
        if not pd.api.types.is_datetime64_any_dtype(self.df["date"]):
            self.df["date"] = pd.to_datetime(self.df["date"], errors='coerce')
        
        df_year = self.df[self.df["date"].dt.year == year].copy()
        df_year["month"] = df_year["date"].dt.month
        grouped = df_year.groupby(["month", "category"])["amount"].sum().unstack(fill_value=0)
        grouped = grouped.reindex(range(1, 13), fill_value=0)
        return grouped
    
    def draw_monthly_report_chart(self, year):
        data = self.monthly_category_report(year)
        ax = data.plot(kind="bar", stacked=False, figsize=(12,6))
        ax.set_title(f"{year} Yılı Aylık Kategori Bazlı Harcamalar")
        ax.set_xlabel("Ay")
        ax.set_ylabel("Toplam Tutar (₺)")
        ax.set_xticklabels([str(m) for m in range(1, 13)], rotation=0)
        plt.legend(title="Kategori")
        plt.tight_layout()
        plt.show()

# Örnek test verisi oluştur
data = {
    "date": [
        "2025-01-15", "2025-01-20", "2025-02-10", "2025-02-15", "2025-03-05",
        "2025-03-10", "2025-04-01", "2025-05-12", "2025-05-15", "2025-06-20",
        "2025-07-25", "2025-07-27", "2025-08-05", "2025-09-10", "2025-10-12",
        "2025-11-20", "2025-12-01"
    ],
    "category": [
        "Gıda", "Ulaşım", "Gıda", "Eğlence", "Eğlence",
        "Ulaşım", "Gıda", "Sağlık", "Gıda", "Eğlence",
        "Gıda", "Sağlık", "Ulaşım", "Gıda", "Eğlence",
        "Sağlık", "Gıda"
    ],
    "amount": [
        200, 150, 300, 120, 250,
        100, 180, 90, 220, 160,
        210, 130, 140, 310, 180,
        100, 230
    ]
}

df = pd.DataFrame(data)

tracker = FinanceTracker(df)
tracker.draw_monthly_report_chart(2025)
