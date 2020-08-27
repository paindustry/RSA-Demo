#!/usr/bin/python2

#-----------------------------------------------------------------+
#	Aplikasi sederhana untuk enkripsi sekaligus dekripsi RSA        |
#-----------------------------------------------------------------+

import random
import sys

class warna:
    biru = '\033[94m'
    hijau = '\033[92m'
    kuning = '\033[93m'
    merah = '\033[91m'
    clear = '\033[0m'

def mod(a, b): #hitung mod
    while b != 0:
        a, b = b, a % b
    return a

def aritmatika_modular(e, phi): # Algoritma Euclidian
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi
    
    while e > 0:
        temp1 = temp_phi/e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        
        x = x2- temp1* x1
        y = d - temp1 * y1
        
        x2 = x1
        x1 = x
        d = y1
        y1 = y
    
    if temp_phi == 1:
        return d + phi

def prima(angka): #cek bil apakah prima
    if angka == 2:
        return True
    if angka < 2 or angka % 2 == 0:
        return False
    for n in xrange(3, int(angka**0.5)+2, 2):
        if angka % n == 0:
            return False
    return True

def generate_kunci(prima1, prima2): #generate public key dan private key
    if not (prima(prima1) and prima(prima2)): # call cek bilangan prima
        sys.tracebacklimit = 0
        raise ValueError(warna.merah+'[!] Bilangan harus prima.'+warna.clear)
    elif prima1 == prima2:
        sys.tracebacklimit = 0
        raise ValueError(warna.merah+'[!] Nggak boleh sama.'+warna.clear)
    n = prima1 * prima2 #Nilai N
    phi = (prima1-1) * (prima2-1) #mencari Fi
    e = random.randrange(1, phi) #ambil bilangan bulat integer antara satu dan Pi (1 < e < Pi) yang juga merupakan koprima dari Pi
    g = mod(e, phi) #menghitung e (mod Pi), e yg sudah di dapatkan nilai 1
    while g != 1: #looping terus sampai dapat nilai 1, jika tidak akan terus mengulang sebanyak nilai yg ada di e
        e = random.randrange(1, phi)
        g = mod(e, phi)
    d = aritmatika_modular(e, phi) #hasil perhitungan algoritma euclidean
    return ((e, n), (d, n)) #(publik keynya, private keynya)

def enkripsi(kunci_private, plaintext): #enkripsi
    key, n = kunci_private
    cipher = [(ord(karakter) ** key) % n for karakter in plaintext] #mendapatkan nilai ascii di tiap karakter dan menghitungnya dengan kunci_private
    return cipher

def dekripsi(kunci_public, ciphertext): #dekripsi
    key, n = kunci_public
    plain = [chr((karakter** key) % n) for karakter in ciphertext] #mengembalikan dari ascii di tiap karakter dan menghitungnya dengan kunci_public
    return ''.join(plain)

if __name__ == '__main__':
	print ("___oO Keripto RSA Oo___")
	print ("=======================")
	print ("Program Encrypt/Decrypt")
	print ("--> 1. Encrypt Pesan   ")
	print ("--> 2. Decrypt Pesan   ")
	print ("--> 3. Keluar          ")
	print ("=======================")
	pilih = input("[+] Masukkan pilihan: ")
	print ("-----------------------")
	if pilih == 1:
		plain = raw_input("=> Masukkan pesan yang mau di encrypt: ")
		p = raw_input("=> Masukkan 2 bilangan prima antara 10 - 100, ex: 17 19: ")
		public, private = generate_kunci(int(p.split(' ',1)[0]), int(p.split(' ',1)[1]))
		encry = enkripsi(private, plain)
		enk = (' ').join(map(lambda x: str(x), encry))
		pbc = (' ').join(map(lambda x: str(x), public))
		print ("-----------------------")
		print ("[*] Plaintext     : "+warna.kuning+str(plain)+warna.clear)
		print ("[*] Bil.prima 1   : "+str(p.split(' ',1)[0]))
		print ("[*] Bil.prima 2   : "+str(p.split(' ',1)[1]))
		print ("[*] Kunci publik  : "+warna.hijau+str(pbc)+warna.clear)
		print ("[*] Kunci private : "+str(private))
		print ("[*] Ciphertext    : "+warna.biru+str(enk)+warna.clear)
		print ("-----------------------")
		print warna.merah+("[!] Aplikasi berhenti")+warna.clear
	elif pilih == 2:
		cipher = raw_input("=> Masukkan Ciphertext: ")
		cipsplit = (map(int ,cipher.split(' ')))
		pubkey = raw_input("=> Masukkan Kunci Publik: ")
		pubsplit = tuple(map(int,pubkey.split(' ')))
		pbc = (' ').join(map(lambda x: str(x), pubsplit))
		decry = dekripsi(pubsplit, cipsplit)
		print ("-----------------------")
		print ("[*] Ciphertext   : "+warna.biru+str(cipher)+warna.clear)
		print ("[*] Kunci Publik : "+warna.hijau+str(pbc)+warna.clear)
		print ("[*] Dekripsi     : "+warna.kuning+str(decry)+warna.clear)
		print ("-----------------------")
		print warna.merah+("[!] Aplikasi berhenti")+warna.clear
	elif pilih == 3:
		print warna.merah+ ("[!] Aplikasi berhenti")+warna.clear
		sys.exit()
	else:
		print warna.merah+("[!] Maaf, pilihan tidak tersedia")+warna.clear
