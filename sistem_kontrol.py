import os
from cryptography.fernet import Fernet

def sistem_hazirlik():
    print("🛡️ CryptoVote Güvenlik Kontrolü Başlatıldı...\n")
    
    # 1. AES Master Key (gizli.key) Kontrolü
    if not os.path.exists("gizli.key"):
        print("⚠️ HATA: 'gizli.key' bulunamadı. Yeni bir AES anahtarı üretiliyor...")
        anahtar = Fernet.generate_key()
        with open("gizli.key", "wb") as f:
            f.write(anahtar)
        print("✅ BAŞARILI: 'gizli.key' oluşturuldu. Bu senin kasanın anahtarıdır!")
    else:
        print("✅ ONAY: AES Anahtarı zaten mevcut.")

    # 2. JSON Dosyalarını Hazırla (Eğer yoklarsa)
    for dosya in ["sandik.json", "secmenler.json"]:
        if not os.path.exists(dosya):
            with open(dosya, "w") as f:
                f.write("[]") # Boş liste olarak başlat
            print(f"✅ ONAY: {dosya} sıfırdan oluşturuldu.")
    
    print("\n🚀 HER ŞEY HAZIR! Artık 'python3 arayuz.py' komutunu çalıştırabilirsin.")

if __name__ == "__main__":
    sistem_hazirlik()
