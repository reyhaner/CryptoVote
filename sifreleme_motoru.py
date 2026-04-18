# [HAFTA 3 - STAGE 3]: AES-256 SİMETRİK ŞİFRELEME MOTORU
from cryptography.fernet import Fernet
import os

class SifrelemeMotoru:
    def __init__(self):
        # Anahtar dosyasını kontrol et, yoksa oluştur (Kasa Anahtarı)
        self.key_file = "gizli.key"
        if not os.path.exists(self.key_file):
            # İlk kez çalışıyorsa yeni bir anahtar üret
            self.key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(self.key)
        else:
            # Varsa mevcut anahtarı oku
            with open(self.key_file, "rb") as f:
                self.key = f.read()
        
        self.fernet = Fernet(self.key)

    def sifrele(self, veri):
        """Metni alır ve AES-256 ile okunamaz hale getirir"""
        return self.fernet.encrypt(veri.encode()).decode()

    def coz(self, sifreli_veri):
        """Şifreli veriyi çözer ve orijinal metni döndürür"""
        return self.fernet.decrypt(sifreli_veri.encode()).decode()

# Hızlı Test (Hoca sorarsa çalıştırıp gösterirsin)
if __name__ == "__main__":
    motor = SifrelemeMotoru()
    test_oy = "A PARTİSİ"
    sifreli = motor.sifrele(test_oy)
    print(f"Orijinal Oy: {test_oy}")
    print(f"Şifreli (Sandıktaki Hali): {sifreli}")
    print(f"Çözülmüş (Kurulun Göreceği): {motor.coz(sifreli)}")
