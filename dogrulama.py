import json
import hashlib
import secrets

def tc_dogrula_ve_token_uret(tc_no):
    # 1. Veritabanını yükle
    try:
        with open("secmenler.json", "r") as f:
            secmenler = json.load(f)
    except FileNotFoundError:
        return "Hata: Seçmen listesi bulunamadı!"

    # 2. TC'yi kontrol et
    secmen_bulundu = False
    for secmen in secmenler:
        if secmen["tc"] == tc_no:
            secmen_bulundu = True
            if secmen["oy_kullandi"]:
                return "Hata: Bu TC ile daha önce oy kullanılmış!"
            
            # 3. Maskeleme ve Token Üretimi (BURASI ÇOK KRİTİK)
            # TC'yi hashliyoruz (Geri döndürülemez maske)
            maskeli_kimlik = hashlib.sha256(tc_no.encode()).hexdigest()
            
            # Güvenli, rastgele bir Token üretiyoruz
            token = secrets.token_hex(16)
            
            # Seçmenin durumunu güncelle (Mükerrer oy engelleme)
            secmen["oy_kullandi"] = True
            
            # Güncel listeyi kaydet
            with open("secmenler.json", "w") as f:
                json.dump(secmenler, f, indent=4)
            
            return {"durum": "basarili", "token": token, "maske": maskeli_kimlik}

    if not secmen_bulundu:
        return "Hata: Geçersiz TC Kimlik No!"

# Test için (Daha sonra arayüze bağlayacağız)
if __name__ == "__main__":
    print("--- 2. Hafta: Kimlik Doğrulama Testi ---")
    test_tc = "12345678901"
    sonuc = tc_dogrula_ve_token_uret(test_tc)
    print(sonuc)
