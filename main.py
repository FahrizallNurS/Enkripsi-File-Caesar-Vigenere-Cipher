# main.py
import os
from crypt_utils import encrypt_file, decrypt_file
from attack_utils import run_full_attack

def input_path(prompt):
    return input(prompt).strip()

def validate_caesar_shift(s):
    try:
        iv = int(s)
    except ValueError:
        return None
    if 0 <= iv <= 25:
        return iv
    return None

def do_encrypt():
    print("\n=== ENCRYPTION (Vigenere -> Caesar) ===")
    infile = input_path("Masukkan path file .txt: ")
    if not os.path.isfile(infile):
        print("[ERROR] File tidak ditemukan:", infile)
        return

    vkey = input("Masukkan kunci Vigenere (A-Z): ").strip()
    s = input("Masukkan kunci Caesar (0-25): ").strip()
    shift = validate_caesar_shift(s)
    if shift is None:
        print("[ERROR] Caesar shift tidak valid.")
        return

    outfile = infile + ".enc"
    try:
        encrypt_file(infile, outfile, vkey, shift)
        print("[OK] Enkripsi selesai →", outfile)
    except Exception as e:
        print("[ERROR] Gagal:", e)

def do_decrypt():
    print("\n=== DECRYPTION (Caesar -> Vigenere) ===")
    infile = input_path("Masukkan path file .enc: ")
    if not os.path.isfile(infile):
        print("[ERROR] File tidak ditemukan:", infile)
        return

    s = input("Masukkan kunci Caesar asli (0-25): ").strip()
    shift = validate_caesar_shift(s)
    if shift is None:
        print("[ERROR] Caesar shift tidak valid.")
        return

    vkey = input("Masukkan kunci Vigenere asli (A-Z): ").strip()
    outfile = infile + ".dec"
    try:
        decrypt_file(infile, outfile, vkey, shift)
        print("[OK] Dekripsi selesai →", outfile)
    except Exception as e:
        print("[ERROR] Gagal:", e)

def do_attack():
    print("\n=== ATTACK MODE (Brute-force Caesar + Vigenere len=2) ===")
    infile = input_path("Masukkan path file .enc: ")
    if not os.path.isfile(infile):
        print("[ERROR] File tidak ditemukan:", infile)
        return

    # read ciphertext
    with open(infile, "r", encoding="utf-8") as f:
        cipher = f.read()

    # output directory (default)
    outdir = infile + "_attack"
    print(f"[*] Output folder: {outdir}")
    print("[*] Caesar brute-force: 26 percobaan")
    print("[*] Vigenere brute-force: key length = 2 (will try length 1 and 2)")
    print("[*] Total percobaan ≈ 26 x (26 + 26^2) = 26 x 702 = 18,252")
    print("[*] Harap tunggu, proses sedang berjalan...")

    try:
        # fixed key length = 2 (tries len 1 and 2)
        run_full_attack(cipher, outdir, max_vig_len=2)
        print("\n[OK] Attack selesai!")
        print("Periksa folder hasil:", outdir)
    except Exception as e:
        print("[ERROR] Attack gagal:", e)

def main():
    print("=== Interactive Vigenere + Caesar Tool ===")
    while True:
        print("\nPilih mode:")
        print("  1. Encrypt (Vigenere -> Caesar)")
        print("  2. Decrypt (Caesar -> Vigenere)")
        print("  3. Attack Mode (Brute-force)")
        print("  4. Exit")

        choice = input("Masukkan pilihan (1/2/3/4): ").strip()
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