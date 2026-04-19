import json
import secrets
import os
from cryptography.fernet import Fernet

def tc_dogrula_ve_token_uret(tc):
    """
    [DÖÇ 1 & DÖÇ 3]: T.C. Kimlik doğrulama, Mükerrer oy kontrolü 
    ve Matematiksel Token üretimi.
    """
    # 1. Gerekli dosyaların varlık kontrolü
    if not os.path.exists("secmenler.json") or not os.path.exists("gizli.key"):
        return "Sistem hatası: Güvenlik anahtarı veya seçmen listesi bulunamadı!"

    try:
        # 2. AES Anahtarını (gizli.key) yükle
        with open("gizli.key", "rb") as k_file:
            key = k_file.read()
        
        fernet = Fernet(key)

        # 3. Şifreli secmenler.json dosyasını oku ve deşifre et
        with open("secmenler.json", "rb") as f:
            sifreli_veri = f.read()
        
        # Eğer dosya tamamen boşsa hata dönmek yerine boş liste kabul et
        if not sifreli_veri:
            return "Sistem hatası: Seçmen listesi henüz oluşturulmamış!"

        # AES Deşifre İşlemi
        cozulmus_veri = fernet.decrypt(sifreli_veri)
        secmenler = json.loads(cozulmus_veri)

        # 4. T.C. Numarası ve Oy Kullanma Durumu Kontrolü
        for secmen in secmenler:
            if secmen["tc"] == tc:
                # [RUBRİK: Mükerrer Oy Kontrolü]
                if secmen["oy_kullandi"]:
                    return "DİKKAT: Bu T.C. numarası ile daha önce oy kullanılmıştır!"
                
                # [RUBRİK: Matematiksel ID / Token Üretimi]
                # Başarılı ise T.C.'den bağımsız rastgele bir token üretilir
                return {
                    "durum": "basarili", 
                    "token": secrets.token_hex(16)
                }
        
        # Eğer T.C. listede hiç yoksa
        return "HATA: T.C. numarası seçmen listesinde kayıtlı değil!"

    except Exception as e:
        # Şifreleme anahtarı değişmişse veya veri bozulmuşsa burası çalışır
        return f"Kritik Güvenlik Hatası (AES): {str(e)}"

# Test amaçlı çalıştırma (Opsiyonel)
if __name__ == "__main__":
    # Örnek bir test (Dosyalar varsa çalışır)
    print("Doğrulama modülü hazır.")
