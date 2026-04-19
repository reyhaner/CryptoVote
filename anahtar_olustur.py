from cryptography.fernet import Fernet

def anahtar_ureten():
    key = Fernet.generate_key()
    with open("gizli.key", "wb") as key_file:
        key_file.write(key)
    print("✅ AES Master Key oluşturuldu: gizli.key")

if __name__ == "__main__":
    anahtar_ureten()
