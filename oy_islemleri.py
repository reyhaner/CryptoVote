# [HAFTA 4 - DÖÇ 4 & 5]: ASİMETRİK ZARFLAMA VE BLOCKCHAIN MOTORU
import json
import hashlib
from asimetrik_motoru import AsimetrikMotor # Daha önce oluşturduğumuz motoru çağırıyoruz

def oy_kullan(secim, token):
    """
    Seçmenin oyunu Kurul'un Public Key'i ile şifreler (DÖÇ 4) 
    ve önceki oyuna bağlayarak zincire ekler (DÖÇ 5).
    """
    motor = AsimetrikMotor()
    
    # 1. ADIM: Oyu Asimetrik Şifrele (Dijital Zarf - DÖÇ 4)
    # "A Partisi" gibi veriyi alır ve sadece Kurulun açabileceği hale getirir.
    sifreli_oy = motor.kamu_anahtari_ile_sifrele(secim)
    
    # 2. ADIM: Mevcut Sandık Verilerini Oku
    try:
        with open("sandik.json", "r") as f:
            sandik = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        sandik = []

    # 3. ADIM: Önceki Oyun Hash Değerini Al (Zincirleme - DÖÇ 5)
    # Eğer ilk oy ise 64 tane sıfır kullanılır, değilse son oyun hash'i alınır.
    onceki_hash = "0" * 64 if len(sandik) == 0 else sandik[-1]["su_anki_hash"]
    
    # 4. ADIM: Yeni Blok Hash'ini Hesapla (Rubrik Formülü)
    # Formül: SHA256(Şifreli_Veri + Önceki_Hash)
    birlesik_veri = f"{sifreli_oy}{onceki_hash}"
    su_anki_hash = hashlib.sha256(birlesik_veri.encode()).hexdigest()

    # 5. ADIM: Yeni Bloğu (Oyu) Oluştur ve Listeye Ekle
    yeni_oy_blogu = {
        "sifreli_oy": sifreli_oy,      # RSA ile şifrelenmiş veri
        "onceki_hash": onceki_hash,    # Zinciri bağlayan parmak izi
        "su_anki_hash": su_anki_hash,  # Bu bloğun parmak izi
        "dogrulama_izi": token[:8]     # Token'ın bir kısmı (izlenebilirlik için)
    }

    sandik.append(yeni_oy_blogu)

    # 6. ADIM: Güncel Sandığı Kaydet
    with open("sandik.json", "w") as f:
        json.dump(sandik, f, indent=4)
    
    return "✅ Oyunuz Blockchain zincirine asimetrik şifreli olarak mühürlendi!"
