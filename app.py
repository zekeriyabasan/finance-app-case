
import pandas as pd
import tkinter as tk
from tkinter import filedialog

from tracker import FinanceTracker

INCOME_CATEGORIES = ["Maaş", "Kira", "Prim", "Diğer"]
EXPENSE_CATEGORIES = ["Market", "Fatura", "Kira", "Ulaşım", "Diğer"]

tracker = FinanceTracker()

def select_file():
        root = tk.Tk()
        root.withdraw()  # Ana pencereyi gizle
        file_path = filedialog.askopenfilename(
            title="CSV dosyası seçin",
            filetypes=[("CSV dosyaları", "*.csv"), ("Tüm dosyalar", "*.*")]
        )
        return file_path

def show_menu():
    print("""
1. KAYIT EKLE
2. KAYIT SİL
3. KAYIT DÜZENLE
4. AYLIK RAPOR
5. YILLIK RAPOR
U. ÇIKIŞ
O. ÇIKIŞ
""")

while True:
    show_menu()
    secim = input("Seçiminiz: ")

    # EKLE
    if secim == "1":
        t = input("Tip (gelir/gider): ").lower()
        if t not in ["gelir", "gider"]:
            print("Hatalı tip.")
            continue

        if t == "gelir":
            print("Kategoriler:", INCOME_CATEGORIES)
            k = input("Kategori seçin: ")
            if k not in INCOME_CATEGORIES:
                print("Geçersiz kategori.")
                continue
        else:
            print("Kategoriler:", EXPENSE_CATEGORIES)
            k = input("Kategori seçin: ")
            if k not in EXPENSE_CATEGORIES:
                print("Geçersiz kategori.")
                continue

        a = input("Tutar: ")
        n = input("Not: ")
        tracker.add_record(t, k, a, n)

    # SİL
    elif secim == "2":
        print(tracker.df)
        idx = int(input("Silinecek index: "))

        if idx in tracker.df.index:
            tracker.delete_record(idx)
            print("Kayıt silindi.")
        else:
            print("Geçersiz index. Böyle bir kayıt yok.")

    #GÜNCELLE
    elif secim == "3":
        print(tracker.df)
        idx = int(input("Düzenlenecek index: "))

        if idx in tracker.df.index:
            alan = input("Alan adı (type, category, amount, note): ")
            if alan in ["type", "category", "amount", "note"]:
                yeni = input("Yeni değer: ")
                tracker.edit_record(idx, **{alan: yeni})
                print("Kayıt güncellendi.")
            else:
                print("Geçersiz alan adı.")
        else:
            print("Geçersiz index. Böyle bir kayıt yok.")

    # AYLIK GRAFİK ÇİZ
    elif secim == "4":
        yil = int(input("Grafiğini görmek istediğiniz yılı girin (örn: 2025): "))
        
        # Tarih sütunu datetime değilse dönüştür
        if not pd.api.types.is_datetime64_any_dtype(tracker.df["date"]):
            tracker.df["date"] = pd.to_datetime(tracker.df["date"], errors="coerce")
        
        # Girilen yıl df içinde geçiyor mu?
        if yil in tracker.df["date"].dt.year.unique():
            tracker.draw_monthly_report_chart(yil)
        else:
            print(f"{yil} yılına ait veri bulunamadı.")

    # YILLIK GRAFİK ÇİZ
    elif secim == "5":
        print(tracker.draw_yearly_report_chart())
    # ÇIKIŞ
    elif secim == "O":
        break
    elif secim == "U":
        csv_path = str(input("Dosya yolunu giriniz: "))
        try:
            tracker.import_csv(csv_path)
            print(f"Dosya başarıyla yüklendi: {csv_path}")
        except Exception as e:
            print(f"Dosya yüklenirken hata oluştu: {e}")
    else:
        print("Geçersiz seçim.")
