# attack_utils.py
import os
import itertools
from crypt_utils import caesar_decrypt, vigenere_decrypt

def ensure_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)

def generate_vigenere_keys(length):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for tup in itertools.product(alphabet, repeat=length):
        yield "".join(tup)

def run_full_attack(ciphertext: str, output_dir: str, max_vig_len=2):

    ensure_dir(output_dir)

    # 1) Caesar brute-force
    for shift in range(26):
        after_caesar = caesar_decrypt(ciphertext, shift)

        caesar_path = os.path.join(output_dir, f"caesar_shift_{shift}.txt")
        with open(caesar_path, "w", encoding="utf-8") as f:
            f.write(after_caesar)

        # 2) Vigenere brute-force key length = 2
        for key in generate_vigenere_keys(2):

            plain = vigenere_decrypt(after_caesar, key)

            out_path = os.path.join(
                output_dir,
                f"dec_shift{shift}_key{key}.txt"
            )
            with open(out_path, "w", encoding="utf-8") as fout:
                fout.write(plain)

    return True