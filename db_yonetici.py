import json
import os

def veritabanini_kur():
    # 1. Seçmen Tablosu: Kimin oy kullanıp kullanmadığını takip eder.
    if not os.path.exists("secmenler.json"):
        baslangic_secmenleri = [
            {"tc": "12345678901", "oy_kullandi": False},
            {"tc": "98765432109", "oy_kullandi": False}
        ]
        with open("secmenler.json", "w") as f:
            json.dump(baslangic_secmenleri, f, indent=4)
        print("✅ secmenler.json (Kimlik Havuzu) oluşturuldu.")

    # 2. Sandık Tablosu: Şifreli oyların ve blockchain parmak izlerinin tutulacağı yer.
    if not os.path.exists("sandik.json"):
        with open("sandik.json", "w") as f:
            json.dump([], f, indent=4)
        print("✅ sandik.json (Dijital Sandık) oluşturuldu.")

if __name__ == "__main__":
    veritabanini_kur()
