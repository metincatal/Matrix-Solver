# Author : Metin ÇATAL
# Date : November 2022

import os
import time
import random

def terminal_temizleyici():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def degisken_atayici(degisken_sayisi):
    degisken_havuzu = ["q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","z","x","c","v","b","n","m"]
    donecek_degiskenler = []
    for i in range(0,degisken_sayisi):
        secilen_degisken = degisken_havuzu[random.randint(0,25-i)]
        donecek_degiskenler.append(secilen_degisken)
        degisken_havuzu.remove(secilen_degisken)
    return donecek_degiskenler

def rasyonel_gosterim(sayi):
    def mutlak_deger(sayi):
        if sayi<0:
            return sayi*-1
        else:
            return sayi
    def asal_mi(sayi):
        asal_mi = True
        for a in range(2,sayi):
            if sayi%a==0:
                asal_mi = False
                break
        return asal_mi
    def asal_carpanlarina_ayirma(sayi):
        asal_carpanlar = []
        while sayi!=1:
            i = 2
            while True:
                if asal_mi(i) and sayi%i==0:
                    asal_carpanlar.append(i)
                    sayi = sayi//i
                    break
                else:
                    i += 1
        return asal_carpanlar

    sayi = round(sayi,2)
    sayi = str(sayi)
    sayi = sayi.split(".")
    if "-" in sayi[0]:
        sayi[1] = str(int(sayi[1])*-1)
    
    if int(sayi[0])==0:
        sayi[0] = int(sayi[1])
    else:
        sayi[0] = ((10**2)*int(sayi[0]))+int(sayi[1])
    sayi[1] = 10**2
    
    carpanlar_sayi = asal_carpanlarina_ayirma(mutlak_deger(sayi[0]))
    carpanlar_onun_kati = asal_carpanlarina_ayirma(sayi[1])
    sayac =0
    for a in carpanlar_sayi:
        if a in carpanlar_onun_kati:
            sayac += 1
    for b in range(0,sayac):
        for c in carpanlar_sayi:
            if c in carpanlar_onun_kati:
                carpanlar_sayi.remove(c)
                carpanlar_onun_kati.remove(c)
    
    carpim_pay = 1
    carpim_payda = 1
    for d in carpanlar_sayi:
        carpim_pay *= d
    if sayi[0]<0:
        carpim_pay *= -1
    for e in carpanlar_onun_kati:
        carpim_payda *= e

    return str(carpim_pay) + "/" + str(carpim_payda)

def matris_ressami(denklem_sayisi,degisken_sayisi,sayilar):
    matris = ""
    kontrol = 0
    for a in range(0,denklem_sayisi):
        for b in range(0,degisken_sayisi):
            matris += f" {int(sayilar[a][b])} "
            kontrol = b
        matris += f"| {int(sayilar[a][kontrol+1])}\n"
    return matris

# 0'ları en alt satıra göndermemiz gerekiyor
def sifir_kontrolu(denklem_sayisi,girilen_sayilar,degisken_sayisi):
    b = 0
    c = 0
    while b<degisken_sayisi:
        for a in range(0,denklem_sayisi):
            if girilen_sayilar[a][b]==0:
                continue
            elif girilen_sayilar[a][b]!=0 and c<a:
                atanacak_sayi_dizisi = girilen_sayilar[c]
                girilen_sayilar[c] = girilen_sayilar[a]
                girilen_sayilar[a] = atanacak_sayi_dizisi
                c += 1
                break
        b += 1
    return [girilen_sayilar,c]

# BİRİM MATRİS
def birim_matrisi(denklem_sayisi):
    birim_matrisi = []
    sutun = 0
    for a in range(0,denklem_sayisi):
        satir = []
        for b in range(0,denklem_sayisi):
            if b==sutun:
                satir.append(1)
            else:
                satir.append(0)
        birim_matrisi.append(satir)
        sutun += 1
    return birim_matrisi

# MİNÖR
def minor(minoru_alinacak_sayinin_indeksi,sayilar,denklem_sayisi):
    for satir in range(int(minoru_alinacak_sayinin_indeksi[1]),denklem_sayisi):
        del sayilar[satir][int(minoru_alinacak_sayinin_indeksi[1])]
    del sayilar[int(minoru_alinacak_sayinin_indeksi[0])]

    return sayilar

# KOFAKTÖR (İŞARETLİ MİNÖR)
def kofaktor(kofaktoru_alinacak_sayinin_indeksi):
    if (int(kofaktoru_alinacak_sayinin_indeksi[0])+int(kofaktoru_alinacak_sayinin_indeksi[1]))%2==0:
        return 1
    else:
        return -1

# DETERMİNANT
def determinant_sifir_kontrolu(sayilar,denklem_sayisi,degisken_sayisi): # determinant 0 ise matrisin tersi yoktur!
    satir = 0
    while satir<denklem_sayisi:
        for a in range(0,denklem_sayisi):
                # satırları gezelim
            # 1-1) Bir satır komple sıfır ise matrisin determinantı sıfırdır.
            satir_sifir_kontrolu = []
            # 1-2) Bir satır diğer bir satırın tam katı ise matrisin determinantı sıfırdır.
            satir_kat_kontrolu = []
            
            for b in range(0,degisken_sayisi):
                # 1-1)
                if sayilar[a][b]!=0:
                    continue
                else:
                    satir_sifir_kontrolu.append(sayilar[a][b])
            
            for c in range(0,degisken_sayisi):
                # 1-2)
                if a==satir:
                    continue
                else:
                    if sayilar[a][c]!=0:
                        satir_kat_kontrolu.append(sayilar[satir][c]/sayilar[a][c])
                    else:
                        satir_kat_kontrolu.append(0)

            # 1-1)
            if len(satir_sifir_kontrolu)==degisken_sayisi:
                return 0
            # 1-2)
            if len(satir_kat_kontrolu)!=0:
                kat = satir_kat_kontrolu[0]
                for x in satir_kat_kontrolu:
                    if kat!=x:
                        kat = x
                        break
                    else:
                        continue
                if kat == satir_kat_kontrolu[0]:
                    return 0
        satir += 1

def determinant(sayilar,denklem_sayisi):
    if determinant_sifir_kontrolu(sayilar,denklem_sayisi,denklem_sayisi)==0:
        return 0
    else:
        if denklem_sayisi==2:
            return (sayilar[0][0]*sayilar[1][1])-(sayilar[0][1]*sayilar[1][0])
        elif denklem_sayisi==3:
            sayilar += [[sayilar[0][0],sayilar[0][1],sayilar[0][2]]]
            sayilar += [[sayilar[1][0],sayilar[1][1],sayilar[1][2]]]
            arti = (sayilar[0][0]*sayilar[1][1]*sayilar[2][2])+(sayilar[1][0]*sayilar[2][1]*sayilar[3][2])+(sayilar[2][0]*sayilar[3][1]*sayilar[4][2])
            eksi = (sayilar[0][2]*sayilar[1][1]*sayilar[2][0])+(sayilar[1][2]*sayilar[2][1]*sayilar[3][0])+(sayilar[2][2]*sayilar[3][1]*sayilar[4][0])
            return arti-eksi
        else:
            carpim = 1
            islem = 0
            satir = 0
            sutun = 0

            while sutun<denklem_sayisi:
                if sayilar[satir][sutun]==0:
                    sutun += 1
                else:
                    for b in range(satir+1,denklem_sayisi):
                        if sayilar[b][sutun]!=0:
                            islem = -1/(sayilar[satir][sutun]/sayilar[b][sutun])
                            for c in range(0,denklem_sayisi):
                                sayilar[b][c] += sayilar[satir][c]*islem
                    satir += 1
                    sutun += 1

            for a in range(0,denklem_sayisi):
                carpim *= sayilar[a][a]
            
            for c in range(0,sifir_kontrolu(denklem_sayisi,sayilar,denklem_sayisi)[1]):
                carpim *= -1

            return int(carpim)

# TERS MATRİS
def ters_matris(sayilar,denklem_sayisi):
    birim_matris = birim_matrisi(denklem_sayisi)
    islem = 0
    satir = 0
    sutun = 0

    while sutun<denklem_sayisi:
        if sayilar[satir][sutun]==0:
            sutun += 1
        else:
            islem = 1/sayilar[satir][sutun]
            for a in range(0,denklem_sayisi):
                sayilar[satir][a] *= islem
                birim_matris[satir][a] *= islem

            for b in range(satir+1,denklem_sayisi):
                islem = sayilar[b][sutun]*-1
                for c in range(0,denklem_sayisi):
                    sayilar[b][c] += sayilar[satir][c]*islem
                    birim_matris[b][c] += birim_matris[satir][c]*islem
            
            satir += 1
            sutun += 1

    kontrol = 0
    kontrol2 = 0
    while sutun>1:
        sutun -= 1
        for d in range(satir-2-kontrol,-1,-1):
            islem = -1*sayilar[d][sutun]
            for e in range(0,denklem_sayisi):
                sayilar[d][e] += sayilar[satir-1-kontrol][e]*islem
                birim_matris[d][e] += birim_matris[satir-1-kontrol][e]*islem
        kontrol += 1
        kontrol2 += 1
    
    for x in range(0,denklem_sayisi):
        for y in range(0,denklem_sayisi):
            birim_matris[x][y] = rasyonel_gosterim(birim_matris[x][y])

    return birim_matris

# GAUSS METODU
def gauss_degiskenlerin_degerlerini_bulma(sayilar,denklem_sayisi,degisken_sayisi,degiskenler):
    degiskenlerin_degerleri = {

    }

    hepsi_sifirmi = True

    for x in range(0,degisken_sayisi+1):
        if sayilar[denklem_sayisi-1][x] != 0:
            hepsi_sifirmi = False
            break
    if hepsi_sifirmi:
        pass
    else:
        for a in range(denklem_sayisi-1,-1,-1):
            islem = 0
            for b in range(degisken_sayisi-1,-1,-1):
                if a==denklem_sayisi-1 and b==degisken_sayisi-1:
                    if sayilar[denklem_sayisi-1][degisken_sayisi] == 0:
                        pass
                    else:
                        degiskenlerin_degerleri.update({
                            degiskenler[b] : sayilar[a][b+1]/sayilar[a][b]
                        })
                else:
                    if sayilar[a][b]==0:
                        continue
                    else:
                        if degiskenler[b] in degiskenlerin_degerleri:
                            islem += sayilar[a][b]*degiskenlerin_degerleri[f"{degiskenler[b]}"]
                        else:
                            degiskenlerin_degerleri.update({
                                degiskenler[b] : sayilar[a][degisken_sayisi]-islem
                            })
    
    print("*Not: Matris gösteriminde ki sayılar orjinallerinin çok uzun olma durumu ve görüntüyü bozma durumundan dolayı yuvarlatılmış hallerini ekrana yazdırır! Yani 0.00002 gibi küçük bir sayı 0 olarak gözüküp yanlış anlaşımlara sebebiyet verebilir. Lütfen orjinalliği bozulmamış 'İşlemler' ve 'Sonuç' kısmını esas alınız!\n\nSonuç;\n")
    
    if sayilar[denklem_sayisi-1][degisken_sayisi-1] == 0:
        print("Lineer denklem sistemi sonsuz çözüme sahip!")
    elif sayilar[denklem_sayisi-1][degisken_sayisi] == 0:
        print("Lineer denklem sisteminin çözümü yoktur!")
    else:
        for i,j in degiskenlerin_degerleri.items():
            print(f"{i} = {j}")

def gauss_islem_yazdirici_1(satir,sutun,sayilar,degisken_sayisi):
    islemin_paydasi = float(sayilar[satir][sutun])
    yazilacak_islem = f"1/{int(sayilar[satir][sutun])} x R{satir+1} --------> R{satir+1}    İşlemler:"
    for a in range(0,degisken_sayisi+1):
        yazilacak_islem += f"  ({float(sayilar[satir][a])}/{islemin_paydasi})"
    print(yazilacak_islem + "\n")

def gauss_islem_yazdirici_2(satir,sutun,sayilar,denklem_sayisi,degisken_sayisi):
    kontrol = 0
    yazilacak_islem = ""
    for a in range(satir+1,denklem_sayisi):
        yazilacak_islem += f"({-1*sayilar[a][sutun]} x R{satir+1-kontrol}) + R{satir+2} --------> R{satir+2}   İşlemler:"
        for b in range(satir-kontrol,degisken_sayisi+1):
            yazilacak_islem += f"   (({-1*sayilar[a][sutun]} x {sayilar[satir-kontrol][b]})+{float(sayilar[satir+1][b])})"
        yazilacak_islem += "\n"
        satir += 1
        kontrol += 1
    print(yazilacak_islem)

def gauss_metodu(denklem_sayisi,degisken_sayisi,girilen_sayilar):
    girilen_sayilar = sifir_kontrolu(denklem_sayisi,girilen_sayilar,degisken_sayisi)[0]
    islem = 0
    satir = 0
    sutun = 0
    gelen_degiskenler = degisken_atayici(degisken_sayisi)

    terminal_temizleyici()
    degiskenleri_yazdirma = ""
    for i in range(0,degisken_sayisi):
        degiskenleri_yazdirma += f" {gelen_degiskenler[i]} "
    print(degiskenleri_yazdirma+" ----> Değişkenler")
    print(matris_ressami(denklem_sayisi,degisken_sayisi,girilen_sayilar))

    while sutun<degisken_sayisi:
        if girilen_sayilar[satir][sutun]==0:
            sutun += 1
        else:
            islem = 1/girilen_sayilar[satir][sutun]

            gauss_islem_yazdirici_1(satir,sutun,girilen_sayilar,degisken_sayisi)
            for a in range(0,degisken_sayisi+1):
                girilen_sayilar[satir][a] *= islem
            print(matris_ressami(denklem_sayisi,degisken_sayisi,girilen_sayilar))

            gauss_islem_yazdirici_2(satir,sutun,girilen_sayilar,denklem_sayisi,degisken_sayisi)
            for b in range(satir+1,denklem_sayisi):
                islem = girilen_sayilar[b][sutun]*-1
                for c in range(0,degisken_sayisi+1):
                    girilen_sayilar[b][c] += girilen_sayilar[satir][c]*islem
            if satir == denklem_sayisi-1:
                son_degiskenler_yazimi = ""
                for l in range(0,degisken_sayisi):
                    son_degiskenler_yazimi += f" {gelen_degiskenler[l]} "
                print(son_degiskenler_yazimi)
                print(matris_ressami(denklem_sayisi,degisken_sayisi,girilen_sayilar))
            else:
                print(matris_ressami(denklem_sayisi,degisken_sayisi,girilen_sayilar))

            satir += 1
            sutun += 1
    gauss_degiskenlerin_degerlerini_bulma(girilen_sayilar,denklem_sayisi,degisken_sayisi,gelen_degiskenler)

# GAUSS JORDAN METHODU
def gauss_jordan_degiskenlerin_degerlerini_bulma(sayilar,denklem_sayisi,degisken_sayisi,degiskenler):
    degiskenlerin_degerleri = {

    }
    
    satir = 0
    sutun = 0

    for a in range(0,degisken_sayisi):
        if sayilar[denklem_sayisi-1][degisken_sayisi] == 0:
            pass
        else:
            degiskenlerin_degerleri.update({
                degiskenler[a] : sayilar[satir][degisken_sayisi]/sayilar[satir][sutun]
            })
        satir += 1
        sutun += 1

    print("*Not: Matris gösteriminde ki sayılar orjinallerinin çok uzun olma durumu ve görüntüyü bozma durumundan dolayı yuvarlatılmış hallerini ekrana yazdırır! Yani 0.00002 gibi küçük bir sayı 0 olarak gözüküp yanlış anlaşımlara sebebiyet verebilir. Lütfen orjinalliği bozulmamış 'İşlemler' ve 'Sonuç' kısmını esas alınız!\n\nSonuç;\n")
    
    if sayilar[denklem_sayisi-1][degisken_sayisi-1] == 0:
        print("Lineer denklem sistemi sonsuz çözüme sahip!")
    elif sayilar[denklem_sayisi-1][degisken_sayisi] == 0:
        print("Lineer denklem sisteminin çözümü yoktur!")
    else:
        for i,j in degiskenlerin_degerleri.items():
            print(f"{i} = {j}")

def gauss_jordan_islem_yazdirici_1(satir,sutun,sayilar,degisken_sayisi):
    gauss_islem_yazdirici_1(satir,sutun,sayilar,degisken_sayisi)

def gauss_jordan_islem_yazdirici_2(satir,sutun,sayilar,denklem_sayisi,degisken_sayisi):
    gauss_islem_yazdirici_2(satir,sutun,sayilar,denklem_sayisi,degisken_sayisi)

def gauss_jordan_islem_yazdirici_3(kontrol,kontrol2,sayilar,denklem_sayisi,degisken_sayisi):
    sutun = degisken_sayisi-1
    satir = denklem_sayisi-2
    yazilacak_islem = ""

    for a in range(satir-kontrol2,-1,-1):
        yazilacak_islem += f"({-1*sayilar[a][sutun-kontrol2]} x R{satir+2-kontrol2}) + R{satir+1-kontrol} --------> R{satir+1-kontrol}   İşlemler:"
        for b in range(0,degisken_sayisi+1):
            yazilacak_islem += f"   (({-1*sayilar[a][sutun-kontrol2]} x {sayilar[satir+1-kontrol2][b]})+{float(sayilar[satir-kontrol][b])})"
        yazilacak_islem += "\n"
        kontrol += 1
    print(yazilacak_islem)

def gauss_jordan_metodu(denklem_sayisi,degisken_sayisi,girilen_sayilar):
    girilen_sayilar = sifir_kontrolu(denklem_sayisi,girilen_sayilar,degisken_sayisi)[0]
    islem = 0
    satir = 0
    sutun = 0
    gelen_degiskenler = degisken_atayici(degisken_sayisi)

    terminal_temizleyici()
    degiskenleri_yazdirma = ""
    for i in range(0,degisken_sayisi):
        degiskenleri_yazdirma += f" {gelen_degiskenler[i]} "
    print(degiskenleri_yazdirma+" ----> Değişkenler")
    print(matris_ressami(denklem_sayisi,degisken_sayisi,girilen_sayilar))

    while sutun<degisken_sayisi:
        if girilen_sayilar[satir][sutun]==0:
            sutun += 1
        else:
            islem = 1/girilen_sayilar[satir][sutun]

            gauss_islem_yazdirici_1(satir,sutun,girilen_sayilar,degisken_sayisi)
            for a in range(0,degisken_sayisi+1):
                girilen_sayilar[satir][a] *= islem
            print(matris_ressami(denklem_sayisi,degisken_sayisi,girilen_sayilar))

            gauss_islem_yazdirici_2(satir,sutun,girilen_sayilar,denklem_sayisi,degisken_sayisi)
            for b in range(satir+1,denklem_sayisi):
                islem = girilen_sayilar[b][sutun]*-1
                for c in range(0,degisken_sayisi+1):
                    girilen_sayilar[b][c] += girilen_sayilar[satir][c]*islem
            print(matris_ressami(denklem_sayisi,degisken_sayisi,girilen_sayilar))
            
            satir += 1
            sutun += 1

    kontrol = 0
    kontrol2 = 0
    while sutun>1:
        sutun -= 1
        gauss_jordan_islem_yazdirici_3(kontrol2,kontrol,girilen_sayilar,denklem_sayisi,degisken_sayisi)
        for d in range(satir-2-kontrol,-1,-1):
            islem = -1*girilen_sayilar[d][sutun]
            for e in range(0,degisken_sayisi+1):
                girilen_sayilar[d][e] += girilen_sayilar[satir-1-kontrol][e]*islem
        kontrol += 1
        kontrol2 += 1
        if sutun==1:
            son_degiskenler_yazimi = ""
            for l in range(0,degisken_sayisi):
                son_degiskenler_yazimi += f" {gelen_degiskenler[l]} "
            print(son_degiskenler_yazimi)
            print(matris_ressami(denklem_sayisi,degisken_sayisi,girilen_sayilar))
        else:
            print(matris_ressami(denklem_sayisi,degisken_sayisi,girilen_sayilar))

    gauss_jordan_degiskenlerin_degerlerini_bulma(girilen_sayilar,denklem_sayisi,degisken_sayisi,gelen_degiskenler)

# CRAMER METHODU
def cramer_metodu(denklem_sayisi,degisken_sayisi,girilen_sayilar):
    pass

# TERS MATRİS METHODU
def ters_matris_methodu():
    pass

# SATIRCA EŞELON FORM
def satirca_eselon_form(denklem_sayisi,degisken_sayisi,girilen_sayilar):
    pass

# SATIRCA İNDİRGENMİŞ EŞELON FORM
def satirca_indirgenmis_eselon_form(denklem_sayisi,degisken_sayisi,girilen_sayilar):
    pass

def isletim_sistemi():
    # başlangıç ekranı
    print("Terminal ekranınız küçük ise büyütünüz!")
    time.sleep(3)
    terminal_temizleyici()

    # seçim ekranı
    while True:
        secim = input("1- Lineer denklem sistemi çözme\n2- Lineer denklem sisteminin determinantını çözme\n3- Lineer denklem sisteminin tersini bulma\n4- Çıkış\nSeçiminiz: ")
        if secim=="1":
            terminal_temizleyici()
            # denklem ve bilinmeyen soru ekranı
            denklem_sayisi = int(input("Lineer denklem sisteminiz kaç denklemli?: "))
            degisken_sayisi = int(input("Lineer denklem sisteminiz kaç bilinmeyenli?: "))
            terminal_temizleyici()

            # terimlerin katsayılarının soru ekranı
            print("Terimlerin katsayılarını giriniz: (*örn)\n 2x+3y=-1\n -x=2\nlineer denklem sisteminin katsayılarının giriş sırası: (2,3,-1,-1,0,2) şeklinde'dir.\n")
            girilen_sayilar = []
            deger=1
            for a in range(0,denklem_sayisi):
                satir = []
                for b in range(1,degisken_sayisi+2):
                    girilen_sayi = int(input(f"{deger}. sayı: "))
                    satir.append(girilen_sayi)
                    deger+=1
                girilen_sayilar.append(satir)
            terminal_temizleyici()

            # çözüm sorusu ekranı
            if denklem_sayisi==degisken_sayisi:
                while True:
                    secim1 = input("1- Gauss yok etme metodu ile\n2- Gauss Jordan yok etme metodu ile\n3- Çıkış\nSeçiminiz: ")
                    if secim1=="1":
                        gauss_metodu(denklem_sayisi,degisken_sayisi,girilen_sayilar)
                        time.sleep(1800)
                        break
                    elif secim1=="2":
                        gauss_jordan_metodu(denklem_sayisi,degisken_sayisi,girilen_sayilar)
                        time.sleep(1800)
                        break
                    # elif secim1=="3":
                    #     cramer_metodu(denklem_sayisi,degisken_sayisi,girilen_sayilar)
                    #     time.sleep(1800)
                    #     break
                    # elif secim1=="4":
                    #     ters_matris(denklem_sayisi,degisken_sayisi,girilen_sayilar)
                    #     time.sleep(1800)
                    #     break
                    elif secim1=="3":
                        break
                    else:
                        terminal_temizleyici()
                        print("Yanlış seçim! Rakamı doğru giriniz!\n")
            # elif denklem_sayisi!=degisken_sayisi:
            #     while True:
            #         secim2 = input("1- Satırca eşelon form yardımıyla\n2- Satırca indirgenmiş form yardımıyla\n3- Çıkış\nSeçiminiz: ")
            #         if secim2=="1":
            #             satirca_eselon_form(denklem_sayisi,degisken_sayisi,girilen_sayilar)
            #             time.sleep(1800)
            #             break
            #         elif secim2=="2":
            #             satirca_indirgenmis_eselon_form(denklem_sayisi,degisken_sayisi,girilen_sayilar)
            #             time.sleep(1800)
            #             break
            #         elif secim2=="3":
            #             break
            #         else:
            #             terminal_temizleyici()
            #             print("Yanlış seçim! Rakamı doğru giriniz!\n")
            else:
                print("Bu yazılım 'şimdilik' kare matrisleri çözüyor!")
        elif secim=="2":
            terminal_temizleyici()
            denklem_sayisi = int(input("Kaç'lık bir matris (*örn: 3): "))
            girilen_sayilar = []
            deger=1
            for a in range(0,denklem_sayisi):
                satir = []
                for b in range(1,denklem_sayisi+1):
                    girilen_sayi = int(input(f"{deger}. sayı: "))
                    satir.append(girilen_sayi)
                    deger+=1
                girilen_sayilar.append(satir)
            terminal_temizleyici()

            matris = ""
            for a in range(0,denklem_sayisi):
                for b in range(0,denklem_sayisi):
                    matris += f"  {int(girilen_sayilar[a][b])} "
                matris += f"\n"
            print(matris + f"\n\n matrisinin determinantı: {determinant(girilen_sayilar,denklem_sayisi)}\n\n")
        elif secim=="3":
            terminal_temizleyici()
            denklem_sayisi = int(input("Kaç'lık bir matris (*örn: 3): "))
            girilen_sayilar = []
            deger=1
            for a in range(0,denklem_sayisi):
                satir = []
                for b in range(1,denklem_sayisi+1):
                    girilen_sayi = int(input(f"{deger}. sayı: "))
                    satir.append(girilen_sayi)
                    deger+=1
                girilen_sayilar.append(satir)
            terminal_temizleyici()
            
            # if determinant(girilen_sayilar,denklem_sayisi)==0:
            #     print("Bu matrisin tersi yoktur!\n")
            # else:
            tersMatris = ""
            for a in range(0,denklem_sayisi):
                for b in range(0,denklem_sayisi):
                    tersMatris += f"  {girilen_sayilar[a][b]} "
                tersMatris += f"\n"

            tersMatris += f"\nMatrisinin tersi;\n\n"
            sayilar = ters_matris(girilen_sayilar,denklem_sayisi)

            for a in range(0,denklem_sayisi):
                for b in range(0,denklem_sayisi):
                    tersMatris += f"  {sayilar[a][b]} "
                tersMatris += f"\n"
            print(tersMatris)
        elif secim=="4":
            break
        else:
            terminal_temizleyici()
            print("Yanlış seçim! Rakamı doğru giriniz!\n")

isletim_sistemi()