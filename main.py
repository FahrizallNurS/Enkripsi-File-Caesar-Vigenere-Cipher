import os
from crypt_utils import encrypt_file_vig_then_caesar, decrypt_file_caesar_then_vig
from attack_utils import run_full_bruteforce

def input_path(msg):
    return input(msg).strip()

def validate_caesar_shift(s):
    try:
        n = int(s)
        return n if 0 <= n <= 25 else None
    except:
        return None

def validate_vig_key(k, length=3):
    k2 = ''.join(ch for ch in k if ch.isalpha())
    return k2.upper() if len(k2) == length else None

def do_encrypt():
    print("\n=== ENCRYPT (Vigenere -> Caesar) ===")
    infile = input_path("Masukkan file .txt (path): ")
    if not os.path.isfile(infile):
        print("[ERROR] File tidak ditemukan.")
        return
    vkey = input("Masukkan kunci Vigenere (3 letters): ").strip()
    vkey_ok = validate_vig_key(vkey, 3)
    if not vkey_ok:
        print("[ERROR] Kunci Vigenere tidak valid (harus 3 huruf).")
        return
    shift = validate_caesar_shift(input("Masukkan kunci Caesar (0-25): ").strip())
    if shift is None:
        print("[ERROR] Caesar shift tidak valid.")
        return
    outfile = infile + ".enc"
    try:
        encrypt_file_vig_then_caesar(infile, outfile, vkey_ok, shift)
    except Exception as e:
        print("[ERROR] Enkripsi gagal:", e)
        return
    print("[OK] Enkripsi selesai →", outfile)

def do_decrypt():
    print("\n=== DECRYPT (Caesar -> Vigenere) ===")
    infile = input_path("Masukkan file .enc (path): ")
    if not os.path.isfile(infile):
        print("[ERROR] File tidak ditemukan.")
        return
    shift = validate_caesar_shift(input("Masukkan kunci Caesar (0-25): ").strip())
    if shift is None:
        print("[ERROR] Caesar shift tidak valid.")
        return
    vkey = input("Masukkan kunci Vigenere (3 letters): ").strip()
    vkey_ok = validate_vig_key(vkey, 3)
    if not vkey_ok:
        print("[ERROR] Kunci Vigenere tidak valid (3 letters).")
        return
    outfile = infile + ".dec"
    try:
        decrypt_file_caesar_then_vig(infile, outfile, shift, vkey_ok)
    except Exception as e:
        print("[ERROR] Dekripsi gagal:", e)
        return
    print("[OK] Dekripsi selesai →", outfile)

def do_attack():
    print("\n=== ATTACK (FULL NESTED BRUTE-FORCE) ===")
    infile = input_path("Masukkan file .enc (path): ")
    if not os.path.isfile(infile):
        print("[ERROR] File tidak ditemukan.")
        return
    with open(infile, 'r', encoding='utf-8') as f:
        cipher = f.read()

    outdir = infile + "_attack"
    print(f"Output akan disimpan di folder: {outdir}")
    print("Mulai brute-force full (26 shifts × 17,576 keys = 456,976 attempts). This may take a while.")
    run_full_bruteforce(cipher, outdir)

def main():
    while True:
        print("\n=== Vigenere + Caesar Toolkit ===")
        print("1) Encrypt (Vigenere -> Caesar)")
        print("2) Decrypt (Caesar -> Vigenere)")
        print("3) Attack (full nested brute-force)")
        print("4) Exit")
        choice = input("Pilih: ").strip()
        if choice == '1':
            do_encrypt()
        elif choice == '2':
            do_decrypt()
        elif choice == '3':
            do_attack()
        elif choice == '4':
            print("Bye.")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()