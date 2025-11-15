# crypt_utils.py
def letter_index(ch: str) -> int:
    return ord(ch.upper()) - ord('A')

def index_to_letter(i: int, is_upper=True) -> str:
    base = ord('A') if is_upper else ord('a')
    return chr((i % 26) + base)

def vigenere_encrypt(plaintext: str, key: str) -> str:
    key = key.upper()
    res = []
    ki = 0
    for ch in plaintext:
        if ch.isalpha():
            p = letter_index(ch)
            k = letter_index(key[ki % len(key)])
            c = (p + k) % 26
            res.append(index_to_letter(c, ch.isupper()))
            ki += 1
        else:
            res.append(ch)
    return ''.join(res)

def vigenere_decrypt(ciphertext: str, key: str) -> str:
    key = key.upper()
    res = []
    ki = 0
    for ch in ciphertext:
        if ch.isalpha():
            c = letter_index(ch)
            k = letter_index(key[ki % len(key)])
            p = (c - k) % 26
            res.append(index_to_letter(p, ch.isupper()))
            ki += 1
        else:
            res.append(ch)
    return ''.join(res)

def caesar_encrypt(text: str, shift: int) -> str:
    out = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            out.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            out.append(ch)
    return ''.join(out)

def caesar_decrypt(text: str, shift: int) -> str:
    return caesar_encrypt(text, (-shift) % 26)

def encrypt_file(input_path: str, output_path: str, vigenere_key: str, caesar_shift: int) -> None:
    with open(input_path, 'r', encoding='utf-8') as f:
        plaintext = f.read()
    step1 = vigenere_encrypt(plaintext, vigenere_key)
    step2 = caesar_encrypt(step1, caesar_shift)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(step2)

def decrypt_file(input_path: str, output_path: str, vigenere_key: str, caesar_shift: int) -> None:
    with open(input_path, 'r', encoding='utf-8') as f:
        cipher = f.read()
    step1 = caesar_decrypt(cipher, caesar_shift)
    plain = vigenere_decrypt(step1, vigenere_key)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(plain)