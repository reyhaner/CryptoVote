# [HAFTA 4 - DÖÇ 4]: ASİMETRİK ŞİFRELEME (RSA) VE DİJİTAL ZARF MOTORU
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import os

class AsimetrikMotor:
    def __init__(self):
        # Rubrik Madde 13/25: Anahtarlar ayrı konfigürasyon dosyalarında saklanır.
        self.private_key_file = "kurul_ozel.pem"
        self.public_key_file = "kurul_genel.pem"

        # Eğer anahtarlar yoksa (ilk kurulum), yeni bir çift oluştur.
        if not os.path.exists(self.private_key_file):
            # 2048-bit RSA anahtar çifti üretilir 
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            
            # Özel Anahtarı (Private Key) PEM formatında kaydet [cite: 31]
            with open(self.private_key_file, "wb") as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))

            # Kamu Anahtarını (Public Key) PEM formatında kaydet 
            public_key = private_key.public_key()
            with open(self.public_key_file, "wb") as f:
                f.write(public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ))

    def kamu_anahtari_ile_sifrele(self, veri):
        """Seçmenin oyunu Kurul'un Public Key'i ile şifreler (DÖÇ 4) """
        # Kayıtlı olan kamu anahtarını dosyadan yükle
        with open(self.public_key_file, "rb") as f:
            public_key = serialization.load_pem_public_key(f.read())
        
        # Oyu şifrele (Dijital Zarf oluştur)
        sifreli = public_key.encrypt(
            veri.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return sifreli.hex()

# Anahtarların oluşturulması için dosya doğrudan çalıştırıldığında tetiklenir
if __name__ == "__main__":
    AsimetrikMotor()
    print("✅ Seçim Kurulu RSA anahtarları üretildi ve dosyalara (PEM) mühürlendi.")
