from tracker import FinanceTracker

tracker = FinanceTracker()

def show_menu():
    print("""
1. Kayıt ekle
2. Kayıt sil
3. Kayıt düzenle
4. Kategori bazlı rapor
5. Aylık rapor
6. Veri görselleştir
7. CSV import
8. CSV export
9. Çıkış
""")

while True:
    show_menu()
    secim = input("Seçiminiz: ")

    if secim == "1":
        t = input("Tip (gelir/gider): ")
        k = input("Kategori: ")
        a = input("Tutar: ")
        n = input("Not: ")
        tracker.add_record(t, k, a, n)
    elif secim == "2":
        print(tracker.df)
        idx = int(input("Silinecek index: "))
        tracker.delete_record(idx)
    elif secim == "3":
        print(tracker.df)
        idx = int(input("Düzenlenecek index: "))
        alan = input("Alan adı (type, category, amount, note): ")
        yeni = input("Yeni değer: ")
        tracker.edit_record(idx, **{alan: yeni})
    elif secim == "4":
        print(tracker.report_by_category())
    elif secim == "5":
        print(tracker.report_by_month())
    elif secim == "6":
        import matplotlib.pyplot as plt
        rapor = tracker.report_by_month().unstack()
        rapor.plot(kind="bar")
        plt.title("Aylık Gelir/Gider")
        plt.tight_layout()
        plt.show()
    elif secim == "7":
        path = input("Import edilecek CSV dosya yolu: ")
        tracker.import_csv(path)
    elif secim == "8":
        path = input("Export edilecek CSV dosya yolu: ")
        tracker.export_csv(path)
    elif secim == "9":
        break
    else:
        print("Geçersiz seçim.")
