import json, hashlib, datetime, os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def oy_kullan(secim, token):
    try:
        with open("gizli.key", "rb") as k: key = k.read()
        fernet = Fernet(key)

        # 1. Seçmeni Güncelle
        with open("secmenler.json", "rb") as f:
            secmenler = json.loads(fernet.decrypt(f.read()))
        
        for s in secmenler:
            if not s["oy_kullandi"]: # Basit eşleşme (Test Modu)
                s["oy_kullandi"] = True
                break
        
        with open("secmenler.json", "wb") as f:
            f.write(fernet.encrypt(json.dumps(secmenler, indent=4).encode()))

        # 2. RSA Şifreleme
        with open("kurul_genel.pem", "rb") as f:
            pub_key = serialization.load_pem_public_key(f.read())

        sifreli_oy = pub_key.encrypt(secim.encode(), padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)).hex()

        # 3. Sandığa Ekle (AES & Blockchain)
        sandik = []
        if os.path.exists("sandik.json") and os.path.getsize("sandik.json") > 0:
            with open("sandik.json", "rb") as f:
                sandik = json.loads(fernet.decrypt(f.read()))

        prev_hash = sandik[-1]["su_anki_hash"] if sandik else "0"*64
        zaman = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        curr_hash = hashlib.sha256(f"{sifreli_oy}{prev_hash}{zaman}".encode()).hexdigest()

        sandik.append({
            "sifreli_oy": sifreli_oy,
            "onceki_hash": prev_hash,
            "zaman_damgasi": zaman,
            "su_anki_hash": curr_hash,
            "token": token
        })

        with open("sandik.json", "wb") as f:
            f.write(fernet.encrypt(json.dumps(sandik, indent=4).encode()))

        return "Oyunuz AES ve RSA ile mühürlendi, Blockchain'e eklendi!"
    except Exception as e: return f"Hata: {e}"
