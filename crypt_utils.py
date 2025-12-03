#mengecek apakah karakter adalah huruf 
def _is_alpha(ch):
    return 'A' <= ch <= 'Z' or 'a' <= ch <= 'z'

#mengubah huruf menjadi angka 
def letter_index(ch: str) -> int:
    return ord(ch.upper()) - ord('A')

#reverse 
def index_to_letter(i: int, is_upper=True) -> str:
    base = ord('A') if is_upper else ord('a')
    return chr((i % 26) + base)

#geser huruf sejumlah 'shift'
def caesar_encrypt(text: str, shift: int) -> str:
    shift = shift % 26
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

def vigenere_encrypt(plaintext: str, key: str) -> str:
    key_clean = ''.join(ch for ch in key if ch.isalpha()).upper()
    if not key_clean:
        raise ValueError("Vigenere key must contain letters.")
    out = []
    ki = 0
    klen = len(key_clean)
    for ch in plaintext:
        if ch.isalpha():
            shift = letter_index(key_clean[ki % klen])
            base = ord('A') if ch.isupper() else ord('a')
            out.append(chr((ord(ch) - base + shift) % 26 + base))
            ki += 1
        else:
            out.append(ch)
    return ''.join(out)

def vigenere_decrypt(ciphertext: str, key: str) -> str:
    key_clean = ''.join(ch for ch in key if ch.isalpha()).upper()
    if not key_clean:
        raise ValueError("Vigenere key must contain letters.")
    out = []
    ki = 0
    klen = len(key_clean)
    for ch in ciphertext:
        if ch.isalpha():
            shift = letter_index(key_clean[ki % klen])
            base = ord('A') if ch.isupper() else ord('a')
            out.append(chr((ord(ch) - base - shift) % 26 + base))
            ki += 1
        else:
            out.append(ch)
    return ''.join(out)

#proses enkripsi dua tahap
def encrypt_file_vig_then_caesar(input_path: str, output_path: str, vigenere_key: str, caesar_shift: int) -> None:
    with open(input_path, 'r', encoding='utf-8') as f:
        plaintext = f.read()
    step1 = vigenere_encrypt(plaintext, vigenere_key)
    step2 = caesar_encrypt(step1, caesar_shift)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(step2)

#reverse
def decrypt_file_caesar_then_vig(input_path: str, output_path: str, caesar_shift: int, vigenere_key: str) -> None:
    with open(input_path, 'r', encoding='utf-8') as f:
        cipher = f.read()
    step1 = caesar_decrypt(cipher, caesar_shift)
    plain = vigenere_decrypt(step1, vigenere_key)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(plain)