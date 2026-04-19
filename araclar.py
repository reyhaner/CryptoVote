import random

def tc_listesi_olustur(adet=100):
    tcler = []
    for _ in range(adet):
        # T.C. Algoritmasına uygun üretim
        haneler = [random.randint(1, 9)] + [random.randint(0, 9) for _ in range(8)]
        tekler = sum(haneler[0::2])
        ciftler = sum(haneler[1::2])
        hane10 = (tekler * 7 - ciftler) % 10
        haneler.append(hane10)
        hane11 = sum(haneler) % 10
        haneler.append(hane11)
        tcler.append("".join(map(str, haneler)))
    
    with open("tcler.txt", "w") as f:
        f.write("\n".join(tcler))
    print(f"✅ {adet} adet T.C. 'tcler.txt' dosyasına kaydedildi.")

if __name__ == "__main__":
    tc_listesi_olustur()
