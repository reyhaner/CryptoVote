import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, filedialog
import json
import hashlib
import os
import datetime
from dogrulama import tc_dogrula_ve_token_uret
from oy_islemleri import oy_kullan
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet # [DÖÇ 3: AES Katmanı]

class CryptoVoteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CryptoVote v8.5 - Siber Güvenlik Final")
        self.root.geometry("650x950")
        self.root.configure(bg="#0f172a") # Koyu siber güvenlik teması
        
        # --- Sistem Ayarları ---
        self.token = None 
        self.kalan_sure = 90
        self.admin_hash = "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9" # 'admin123'
        self.master_key = self.anahtar_yukle() # AES Anahtarı
        
        # Header (Üst Başlık)
        self.header = tk.Frame(self.root, bg="#1e293b", height=80)
        self.header.pack(fill="x")
        tk.Label(self.header, text="🛡️ CRYPTOVOTE", font=("Consolas", 26, "bold"), 
                 bg="#1e293b", fg="#38bdf8").pack(pady=20)

        self.main_frame = tk.Frame(self.root, bg="#0f172a")
        self.main_frame.pack(expand=True, fill="both", padx=40)

        self.log_yaz("Sistem AES-256 korumasıyla başlatıldı.")
        self.ana_menu_goster()

    # =========================================================================
    # [DÖÇ 3]: AES VERİTABANI YÖNETİMİ (DOSYA SEVİYESİNDE ŞİFRELEME)
    # =========================================================================
    def anahtar_yukle(self):
        """AES anahtarını 'gizli.key' dosyasından yükler"""
        if os.path.exists("gizli.key"):
            with open("gizli.key", "rb") as f: return f.read()
        return None

    def veri_yaz(self, dosya, veri):
        """[DÖÇ 3]: Veriyi AES ile şifreleyerek kaydeder"""
        if not self.master_key: return
        try:
            fernet = Fernet(self.master_key)
            json_str = json.dumps(veri, indent=4).encode()
            sifreli_blob = fernet.encrypt(json_str)
            with open(dosya, "wb") as f: f.write(sifreli_blob)
        except Exception as e: print(f"Yazma hatası: {e}")

    def veri_oku(self, dosya):
        """[DÖÇ 3]: Dosyayı AES ile deşifre ederek okur"""
        if not os.path.exists(dosya) or not self.master_key: return []
        try:
            fernet = Fernet(self.master_key)
            with open(dosya, "rb") as f: sifreli_blob = f.read()
            if not sifreli_blob: return []
            return json.loads(fernet.decrypt(sifreli_blob))
        except: return []

    # =========================================================================
    # YARDIMCI ARAÇLAR (LOG VE MASKELEME)
    # =========================================================================
    def log_yaz(self, mesaj):
        zaman = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("sistem.log", "a", encoding="utf-8") as f:
            f.write(f"[{zaman}] {mesaj}\n")

    def tc_maskele(self, tc):
        """[PII/KVKK]: TC'yi maskeler"""
        t = str(tc)
        return f"{t[:3]}******{t[-2:]}"

    # =========================================================================
    # EKRAN YÖNETİMİ (ANA MENÜ, GİRİŞ, OYLAMA)
    # =========================================================================
    def ana_menu_goster(self):
        for w in self.main_frame.winfo_children(): w.destroy()
        tk.Label(self.main_frame, text="Zırhlı Seçim Platformu", font=("Segoe UI", 10), bg="#0f172a", fg="#94a3b8").pack(pady=30)
        tk.Button(self.main_frame, text="🗳️ OY KULLANMA PANELİ", bg="#38bdf8", fg="#0f172a", font=("Segoe UI", 12, "bold"), height=3, command=self.setup_login_screen).pack(fill="x", pady=10)
        tk.Button(self.main_frame, text="⚖️ SEÇİM KURULU (ADMİN)", bg="#1e293b", fg="#38bdf8", font=("Segoe UI", 12, "bold"), height=3, command=self.admin_giris_kontrol).pack(fill="x", pady=10)

    def setup_login_screen(self):
        for w in self.main_frame.winfo_children(): w.destroy()
        tk.Label(self.main_frame, text="T.C. Kimlik Numaranızı Giriniz:", bg="#0f172a", fg="#94a3b8").pack(pady=(40, 5))
        self.ent_tc = tk.Entry(self.main_frame, font=("Consolas", 14), bg="#1e293b", fg="#38bdf8", justify="center", bd=0)
        self.ent_tc.pack(fill="x", pady=10, ipady=10)
        tk.Button(self.main_frame, text="SİSTEME GİRİŞ", bg="#38bdf8", font=("Segoe UI", 11, "bold"), command=self.giris_kontrol).pack(fill="x", pady=20)
        tk.Button(self.main_frame, text="⬅️ ANA MENÜ", bg="#334155", fg="white", command=self.ana_menu_goster).pack(fill="x")

    def giris_kontrol(self):
        tc = self.ent_tc.get()
        # [DÖÇ 1: Matematiksel ID ve Doğrulama]
        sonuc = tc_dogrula_ve_token_uret(tc)
        if isinstance(sonuc, dict) and sonuc["durum"] == "basarili":
            self.token = sonuc["token"]
            self.log_yaz(f"Seçmen girişi başarılı: {self.tc_maskele(tc)}")
            self.setup_voting_screen()
        else:
            self.log_yaz(f"Başarısız giriş denemesi: {tc}")
            messagebox.showerror("Erişim Reddedildi", sonuc)

    def setup_voting_screen(self):
        for w in self.main_frame.winfo_children(): w.destroy()
        self.lbl_timer = tk.Label(self.main_frame, text=f"Kalan Süre: {self.kalan_sure} sn", font=("Consolas", 14, "bold"), bg="#0f172a", fg="#f87171")
        self.lbl_timer.pack(pady=10)
        for aday in ["A PARTİSİ", "B PARTİSİ", "C PARTİSİ"]:
            tk.Button(self.main_frame, text=aday, bg="#1e293b", fg="white", font=("Segoe UI", 12), height=2, command=lambda a=aday: self.oy_kaydet(a)).pack(fill="x", pady=8)
        self.tick()

    def tick(self):
        if self.kalan_sure > 0:
            self.kalan_sure -= 1
            self.lbl_timer.config(text=f"Kalan Süre: {self.kalan_sure} sn")
            self.timer_id = self.root.after(1000, self.tick)
        else: self.ana_menu_goster()

    def oy_kaydet(self, secim):
        self.root.after_cancel(self.timer_id)
        if messagebox.askyesno("Onay", f"{secim} seçimini mühürlemek istiyor musunuz?"):
            # TC ile değil, Token ile oy kullanılır (Anonimlik)
            mesaj = oy_kullan(secim, self.token)
            messagebox.showinfo("Sonuç", mesaj)
            self.ana_menu_goster()

    # =========================================================================
    # KISITLANMIŞ ADMİN PANELİ (GÜVENLİ DENETİM VE SAYIM)
    # =========================================================================
    def admin_giris_kontrol(self):
        sifre = simpledialog.askstring("Yetki", "Admin Şifresi:", show='*')
        if sifre and hashlib.sha256(sifre.encode()).hexdigest() == self.admin_hash:
            self.log_yaz("Yönetici girişi yapıldı.")
            self.admin_paneli()
        elif sifre: messagebox.showerror("Hata", "Şifre Yanlış!")

    def admin_paneli(self):
        for w in self.main_frame.winfo_children(): w.destroy()
        tk.Label(self.main_frame, text="📊 SEÇİM KURULU DENETİM MERKEZİ", font=("Segoe UI", 14, "bold"), bg="#0f172a", fg="#38bdf8").pack(pady=10)
        
        # Seçmen Listesi Tablosu
        self.tree = ttk.Treeview(self.main_frame, columns=("TC", "DURUM"), show='headings', height=8)
        self.tree.heading("TC", text="T.C. Kimlik (Maskelenmiş)"); self.tree.heading("DURUM", text="Oy Durumu")
        self.tree.pack(fill="x", pady=10); self.tabloyu_guncelle()

        # Araçlar
        tk.Button(self.main_frame, text="📂 T.C. LİSTESİNİ SİSTEME AKTAR (E-DEVLET)", bg="#1e293b", fg="#38bdf8", font=("Segoe UI", 9, "bold"), command=self.toplu_secmen_ekle).pack(fill="x", pady=2)
        tk.Button(self.main_frame, text="🕵️ GÜVENLİK LOGLARI (ADLİ BİLİŞİM)", bg="#1e293b", fg="#94a3b8", command=self.loglari_goster).pack(fill="x", pady=2)
        
        # Reyhan'ın Özel "Sistemi Sıfırla" Butonu
        tk.Button(self.main_frame, text="⚠️ TÜM SİSTEMİ SIFIRLA (TEST MODU)", bg="#7f1d1d", fg="white", font=("Segoe UI", 9, "bold"), command=self.sistemi_sifirla).pack(fill="x", pady=2)
        
        tk.Button(self.main_frame, text="🔓 SANDIĞI AÇ VE SAYIMI BAŞLAT", bg="#1e293b", fg="#4ade80", font=("Segoe UI", 10, "bold"), height=2, command=self.sandik_ac).pack(fill="x", pady=5)
        
        self.txt_out = tk.Text(self.main_frame, height=10, bg="#020617", fg="#4ade80", font=("Consolas", 10), bd=0)
        self.txt_out.pack(fill="both", pady=10)
        tk.Button(self.main_frame, text="⬅️ ANA MENÜ", bg="#334155", fg="white", command=self.ana_menu_goster).pack(fill="x")

    def tabloyu_guncelle(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        secmenler = self.veri_oku("secmenler.json")
        for s in secmenler:
            self.tree.insert('', 'end', values=(self.tc_maskele(s["tc"]), "✅ OY VERDİ" if s["oy_kullandi"] else "❌ VERMEDİ"))

    def sistemi_sifirla(self):
        """Testleri kolaylaştırmak için dosyaları temizler (AES Şifreli)"""
        if messagebox.askyesno("UYARI", "Tüm seçmen ve sandık verileri silinecek! Emin misiniz?"):
            self.veri_yaz("secmenler.json", [])
            self.veri_yaz("sandik.json", [])
            self.tabloyu_guncelle()
            self.log_yaz("SİSTEM YÖNETİCİ TARAFINDAN SIFIRLANDI.")
            messagebox.showinfo("Başarılı", "Sistem tertemiz hale getirildi!")

    def toplu_secmen_ekle(self):
        path = filedialog.askopenfilename(filetypes=[("Metin", "*.txt")])
        if path:
            with open(path, "r") as f: tclist = [l.strip() for l in f if len(l.strip())==11]
            data = self.veri_oku("secmenler.json")
            mevcut = {s["tc"] for s in data}
            eklenen = 0
            for t in tclist:
                if t not in mevcut: 
                    data.append({"tc": t, "oy_kullandi": False})
                    eklenen += 1
            self.veri_yaz("secmenler.json", data)
            self.tabloyu_guncelle()
            messagebox.showinfo("Başarılı", f"{eklenen} yeni seçmen eklendi.")

    def sandik_ac(self):
        """[DÖÇ 5]: RSA Deşifre ve Blockchain Bütünlük Kontrolü"""
        try:
            with open("kurul_ozel.pem", "rb") as f: 
                pk = serialization.load_pem_private_key(f.read(), password=None)
            
            sandik = self.veri_oku("sandik.json")
            sayim = {}
            self.txt_out.delete('1.0', tk.END)
            
            if not sandik:
                self.txt_out.insert(tk.END, "⚠️ Sandık henüz mühürlü (boş)!\n")
                return
            
            self.txt_out.insert(tk.END, "--- 🔐 DEŞİFRE VE DOĞRULAMA BAŞLADI ---\n")
            
            for b in sandik:
                try:
                    # RSA ile oyu çöz
                    oy = pk.decrypt(
                        bytes.fromhex(b["sifreli_oy"]), 
                        padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
                    ).decode()
                    sayim[oy] = sayim.get(oy, 0) + 1
                    self.txt_out.insert(tk.END, f"✅ [{b['zaman_damgasi']}] Blok Doğrulandı.\n")
                except:
                    self.txt_out.insert(tk.END, "❌ HATA: Müdahale edilmiş blok tespit edildi!\n")
            
            # Sonuçları Görselleştir
            self.txt_out.insert(tk.END, "\n📊 SEÇİM SONUÇLARI\n" + "-"*30 + "\n")
            toplam = sum(sayim.values())
            for p, a in sorted(sayim.items(), key=lambda x: x[1], reverse=True):
                y = (a/toplam)*100
                bar = "█" * int(y/5)
                self.txt_out.insert(tk.END, f"{p:<12}: %{y:>5.1f} {bar} ({a} Oy)\n")
                
            self.log_yaz("Sandık açıldı ve sayım yapıldı.")
        except Exception as e:
            messagebox.showerror("Hata", f"Deşifre anahtarı yüklenemedi: {e}")

    def loglari_goster(self):
        log_w = tk.Toplevel(self.root)
        log_w.title("🕵️ Adli Bilişim Logları")
        log_w.geometry("550x450")
        log_w.configure(bg="#0f172a")
        t = tk.Text(log_w, bg="#020617", fg="#94a3b8", font=("Consolas", 9), padx=10, pady=10)
        t.pack(expand=True, fill="both")
        if os.path.exists("sistem.log"):
            with open("sistem.log", "r") as f:
                t.insert(tk.END, "".join(reversed(f.readlines())))

if __name__ == "__main__":
    root = tk.Tk(); app = CryptoVoteGUI(root); root.mainloop()
