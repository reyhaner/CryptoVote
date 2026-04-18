# =========================================================================
# [HAFTA 1-5]: CRYPTOVOTE TAM ENTEGRE GÜVENLİ OYLAMA ARAYÜZÜ (GUI)
# =========================================================================
import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import hashlib
from dogrulama import tc_dogrula_ve_token_uret  # Hafta 2 (Rubrik 12)
from oy_islemleri import oy_kullan            # Hafta 4 (Rubrik 14)
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

class CryptoVoteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CryptoVote v1.0 - Secure Systems")
        self.root.geometry("500x750")
        self.root.configure(bg="#121212")
        self.token = None 

        # --- Sabit Üst Başlık ---
        self.header = tk.Frame(self.root, bg="#1f1f1f", height=100)
        self.header.pack(fill="x", side="top")
        tk.Label(
            self.header, text="🛡️ CRYPTOVOTE", 
            font=("Consolas", 24, "bold"), bg="#1f1f1f", fg="#00d4ff"
        ).pack(pady=25)

        # --- İçerik Alanı ---
        self.container = tk.Frame(self.root, bg="#121212")
        self.container.pack(expand=True, fill="both", padx=40)

        self.ana_menu_goster()

    def ana_menu_goster(self):
        """Sistemin ana karşılama menüsü"""
        for widget in self.container.winfo_children(): widget.destroy()

        tk.Label(self.container, text="Hoş Geldiniz. Lütfen işlem seçiniz:", font=("Segoe UI", 10), bg="#121212", fg="#aaaaaa").pack(pady=30)

        tk.Button(
            self.container, text="🗳️ OY KULLANMA PANELİ", 
            bg="#00d4ff", fg="black", font=("Segoe UI", 12, "bold"), 
            height=3, cursor="hand2", command=self.setup_login_screen
        ).pack(fill="x", pady=15)

        tk.Button(
            self.container, text="⚖️ SEÇİM KURULU (ADMİN)", 
            bg="#1f1f1f", fg="#00d4ff", font=("Segoe UI", 12, "bold"), 
            height=3, cursor="hand2", command=self.admin_paneli
        ).pack(fill="x", pady=15)

    def setup_login_screen(self):
        """Hafta 2: Seçmen Kimlik Doğrulama Ekranı"""
        for widget in self.container.winfo_children(): widget.destroy()
        
        tk.Label(self.container, text="T.C. Kimlik Numaranızı Giriniz:", font=("Segoe UI", 10), bg="#121212", fg="#aaaaaa").pack(pady=(40, 5))
        
        self.ent_tc = tk.Entry(
            self.container, font=("Consolas", 14), 
            bg="#2c2c2c", fg="#00d4ff", insertbackground="white", bd=0, justify="center"
        )
        self.ent_tc.pack(fill="x", pady=10, ipady=10)

        tk.Button(self.container, text="GİRİŞ YAP VE DOĞRULA", bg="#00d4ff", fg="black", font=("Segoe UI", 11, "bold"), height=2, command=self.giris_kontrol).pack(fill="x", pady=20)
        tk.Button(self.container, text="⬅️ ANA MENÜ", bg="#333333", fg="white", command=self.ana_menu_goster).pack(fill="x")

    def giris_kontrol(self):
        tc = self.ent_tc.get()
        sonuc = tc_dogrula_ve_token_uret(tc)

        if isinstance(sonuc, dict) and sonuc["durum"] == "basarili":
            self.token = sonuc["token"]
            messagebox.showinfo("Başarılı", "Kimlik Doğrulandı! Oylama Ekranı Açılıyor.")
            self.setup_voting_screen()
        else:
            messagebox.showerror("Hata", sonuc)

    def setup_voting_screen(self):
        """Hafta 1: Oy Kullanma Ekranı (Aday Seçimi)"""
        for widget in self.container.winfo_children(): widget.destroy()

        tk.Label(self.container, text="ADAYINIZI SEÇİNİZ", font=("Segoe UI", 14, "bold"), bg="#121212", fg="#00d4ff").pack(pady=30)

        adaylar = ["A PARTİSİ", "B PARTİSİ", "C PARTİSİ"]
        for aday in adaylar:
            tk.Button(
                self.container, text=aday, bg="#1f1f1f", fg="white", 
                font=("Segoe UI", 12), height=2, bd=1, cursor="hand2",
                activebackground="#00d4ff", activeforeground="black",
                command=lambda a=aday: self.oy_onay_al(a)
            ).pack(fill="x", pady=8)

    def oy_onay_al(self, secim):
        """Hafta 4: Oyu şifrele ve Blockchain zincirine ekle"""
        if messagebox.askyesno("Oylama Onayı", f"{secim} için oyunuzu onaylıyor musunuz?"):
            mesaj = oy_kullan(secim, self.token)
            messagebox.showinfo("Blockchain Onayı", mesaj)
            self.ana_menu_goster()

    # =========================================================================
    # SEÇİM KURULU (ADMİN) PANELİ - HAFTA 5 / RİSKLİ ALAN
    # =========================================================================
    def admin_paneli(self):
        """Admin paneline giriş için şifre kontrolü ve panel tasarımı"""
        admin_sifre = simpledialog.askstring("Yetkilendirme", "Yönetici Şifresini Giriniz:", show='*')
        
        # Siber güvenlik klasiği yönetici şifresi
        if admin_sifre == "admin123":
            for widget in self.container.winfo_children(): widget.destroy()

            tk.Label(self.container, text="SEÇİM KURULU DENETİM PANELİ", font=("Segoe UI", 12, "bold"), bg="#121212", fg="#ff4444").pack(pady=20)

            # Manipülasyon Testi Butonu (Rubrik Madde 42)
            tk.Button(self.container, text="⛓️ ZİNCİR BÜTÜNLÜĞÜNÜ DOĞRULA", bg="#ff4444", fg="white", font=("Segoe UI", 10, "bold"), height=2, command=self.blockchain_kontrol).pack(fill="x", pady=10)

            # Sandık Açma Butonu (Rubrik Madde 40)
            tk.Button(self.container, text="🔓 SANDIĞI AÇ VE OYLARI SAY", bg="#44ff44", fg="black", font=("Segoe UI", 10, "bold"), height=2, command=self.sandik_verilerini_ac).pack(fill="x", pady=10)

            # Sonuçların görüneceği terminal alanı
            self.txt_output = tk.Text(self.container, height=12, bg="#000000", fg="#00ff00", font=("Consolas", 9), bd=0)
            self.txt_output.pack(fill="both", pady=10)

            tk.Button(self.container, text="⬅️ ANA MENÜ", bg="#333333", fg="white", command=self.ana_menu_goster).pack(fill="x")
        else:
            if admin_sifre is not None:
                messagebox.showerror("Yetkisiz Erişim", "Hatalı şifre! Erişim engellendi.")

    def blockchain_kontrol(self):
        """Rubrik Madde 42: Zincirleme Bütünlük ve Manipülasyon Testi"""
        try:
            with open("sandik.json", "r") as f: sandik = json.load(f)
            hata_var = False
            for i in range(len(sandik)):
                blok = sandik[i]
                # Rubrikteki formül: Hash(Veri + Önceki Hash)
                veriler = f"{blok['sifreli_oy']}{blok['onceki_hash']}"
                hesap_hash = hashlib.sha256(veriler.encode()).hexdigest()
                
                if hesap_hash != blok['su_anki_hash']:
                    messagebox.showerror("KRİTİK UYARI", f"Blok {i+1} manipüle edilmiş! Zincir bütünlüğü bozuldu.")
                    hata_var = True
                    break
            if not hata_var: messagebox.showinfo("Bütünlük Onaylandı", "Blockchain zinciri sağlam. Hiçbir müdahale tespit edilmedi.")
        except Exception as e: messagebox.showerror("Hata", f"Dosya hatası: {e}")

    def sandik_verilerini_ac(self):
        """Rubrik Madde 40: Canlı Demo - Sandık Açma (Asimetrik Deşifre)"""
        try:
            with open("kurul_ozel.pem", "rb") as f:
                ozel_anahtar = serialization.load_pem_private_key(f.read(), password=None)
            with open("sandik.json", "r") as f: sandik = json.load(f)
            
            sayim = {}
            self.txt_output.delete('1.0', tk.END)
            self.txt_output.insert(tk.END, "--- Oylar Deşifre Ediliyor ---\n")
            
            for blok in sandik:
                # Oyu Private Key ile açıyoruz (DÖÇ 4)
                cozulen = ozel_anahtar.decrypt(
                    bytes.fromhex(blok["sifreli_oy"]),
                    padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
                ).decode()
                sayim[cozulen] = sayim.get(cozulen, 0) + 1
            
            self.txt_output.insert(tk.END, f"\nSEÇİM SONUÇLARI:\n{json.dumps(sayim, indent=4)}")
        except Exception as e: messagebox.showerror("Hata", "Özel anahtar yüklenemedi veya veri bozuk!")

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoVoteGUI(root)
    root.mainloop()
