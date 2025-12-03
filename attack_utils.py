import os
import time
from crypt_utils import caesar_decrypt, vigenere_decrypt

#generator untuk menghasilkam kunci vigenere
def generate_keys_len3():
    for a in range(26):
        ca = chr(65 + a)
        for b in range(26):
            cb = chr(65 + b)
            for c in range(26):
                yield ca + cb + chr(65 + c)

#make directory for output
def ensure_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)

def run_full_bruteforce(ciphertext: str, outdir: str):
    """
    Full pipeline:
    - write hasil_caesar.txt with intermediate ciphertexts for shifts 0..25
    - for each shift, try all 26^3 keys; write each attempt to hasil_vigenere.txt in chronological order:
        "Shift X | Key YYY -> <plaintext>"
    - print progress per shift and every N keys inside shift
    """
    ensure_dir(outdir)
    caesar_file = os.path.join(outdir, "hasil_caesar.txt")
    vigenere_file = os.path.join(outdir, "hasil_vigenere.txt")

#atack caesar
    with open(caesar_file, "w", encoding='utf-8') as cf:
        cf.write("==== HASIL BRUTE FORCE CAESAR ====\n\n")
        for shift in range(26):
            mid = caesar_decrypt(ciphertext, shift)
            cf.write(f"[Shift {shift}]\nCiphertext: {mid.replace(chr(10), '\\n')}\n\n")

#attackk vigenere
    total_attempts = 26 * (26**3)
    print(f"[INFO] Starting nested brute-force: total attempts = {total_attempts:,}")
    start_time = time.time()
    attempts_done = 0

    with open(vigenere_file, "w", encoding='utf-8') as vf:
        vf.write("==== HASIL BRUTE FORCE VIGENERE ====\n\n")
        for shift in range(26):
            mid = caesar_decrypt(ciphertext, shift)
            print(f"\n[Shift {shift}] Starting 17,576 keys...")  
            vf.write(f"--- SHIFT {shift} ---\n")
            last_report = 0
            for idx, key in enumerate(generate_keys_len3(), start=1):
                pt = vigenere_decrypt(mid, key)
                vf.write(f"Shift {shift} | Key {key} ->\n{pt}\n\n")

                attempts_done += 1
                if idx % 1000 == 0:
                    elapsed = time.time() - start_time
                    pct = attempts_done / total_attempts * 100
                    print(f"  [Shift {shift}] tested {idx:,}/17,576 keys | overall {attempts_done:,}/{total_attempts:,} ({pct:.2f}%) | elapsed {int(elapsed)}s")

            print(f"  [Shift {shift}] done (17,576 keys).")
    elapsed_total = time.time() - start_time
    print(f"\n[INFO] Brute-force finished. Total attempts: {attempts_done:,}. Time: {int(elapsed_total)}s")
    print(f"Output files:\n - {caesar_file}\n - {vigenere_file}")
    return caesar_file, vigenere_file