import tkinter as tk
from tkinter import messagebox

class CryptoVoteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CryptoVote v1.0 - Secure Systems")
        self.root.geometry("450x550")
        self.root.configure(bg="#121212")  # Koyu arka plan (Siber Güvenlik Teması)

        # Üst Başlık Alanı
        self.header_frame = tk.Frame(root, bg="#1f1f1f", height=100)
        self.header_frame.pack(fill="x")

        self.lbl_title = tk.Label(
            self.header_frame, 
            text="🛡️ CRYPTOVOTE", 
            font=("Consolas", 24, "bold"), 
            bg="#1f1f1f", 
            fg="#00d4ff"  # Neon Mavi
        )
        self.lbl_title.pack(pady=20)

        # Durum Çizgisi
        self.status_line = tk.Frame(root, bg="#00d4ff", height=2)
        self.status_line.pack(fill="x")

        # Orta Alan (İçerik)
        self.content_frame = tk.Frame(root, bg="#121212")
        self.content_frame.pack(expand=True)

        self.lbl_welcome = tk.Label(
            self.content_frame, 
            text="Güvenli Oylama Sistemine Hoş Geldiniz", 
            font=("Segoe UI", 12), 
            bg="#121212", 
            fg="#ffffff"
        )
        self.lbl_welcome.pack(pady=30)

        # BUTONLAR - Daha modern ve geniş
        btn_style = {
            "font": ("Segoe UI", 11, "bold"),
            "width": 25,
            "height": 2,
            "bd": 0,
            "cursor": "hand2",
            "activebackground": "#00a8cc"
        }

        self.btn_oy = tk.Button(
            self.content_frame, 
            text="🗳️ OY KULLANMA PANELİ", 
            bg="#00d4ff", 
            fg="#000000",
            command=self.oy_paneli,
            **btn_style
        )
        self.btn_oy.pack(pady=15)

        self.btn_kurul = tk.Button(
            self.content_frame, 
            text="🔐 SEÇİM KURULU GİRİŞİ", 
            bg="#2c2c2c", 
            fg="#ffffff",
            command=self.kurul_paneli,
            **btn_style
        )
        self.btn_kurul.pack(pady=10)

        # Alt Bilgi (Footer)
        self.lbl_footer = tk.Label(
            root, 
            text="Sistem Durumu: ÇALIŞIYOR | AES-256 Aktif", 
            font=("Consolas", 9), 
            bg="#121212", 
            fg="#555555"
        )
        self.lbl_footer.pack(side="bottom", pady=20)

    def oy_paneli(self):
        messagebox.showinfo("Erişim İstendi", "Seçmen Kimlik Doğrulama modülü (Hafta 2) yükleniyor...")

    def kurul_paneli(self):
        messagebox.showwarning("Yetki Hatası", "Bu alana girmek için RSA-Private Key gereklidir!")

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoVoteGUI(root)
    root.mainloop()
