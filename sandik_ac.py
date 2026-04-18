# [HAFTA 5]: SANDIK AÇMA VE SONUÇ DOĞRULAMA MOTORU
import json
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def sandigi_ac():
    # 1. Özel Anahtarı (Private Key) Yükle [cite: 31]
    with open("kurul_ozel.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    # 2. Sandık Verilerini Oku
    with open("sandik.json", "r") as f:
        sandik = json.load(f)

    sonuclar = {}

    print("--- SEÇİM SONUÇLARI DOĞRULANIYOR ---")
    for blok in sandik:
        # 3. Her oyu Private Key ile çöz (Decryption) 
        sifreli_veri = bytes.fromhex(blok["sifreli_oy"])
        cozulden_oy = private_key.decrypt(
            sifreli_veri,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode()

        # 4. Sayım Yap
        sonuclar[cozulden_oy] = sonuclar.get(cozulden_oy, 0) + 1
    
    return sonuclar

if __name__ == "__main__":
    skor = sandigi_ac()
    print(f"Final Tablosu: {skor}")
