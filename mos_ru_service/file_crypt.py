import hashlib

from datetime import datetime

def salsa_20_xor_bytes():
    pass


def n_string(string, n):
    hash = hashlib.sha512()
    hash.update(string.encode('utf-8'))
    return hash.digest()[:n]


def encryption(iv: str, key: str, filename: str) -> bool:
    try:
        iv = n_string(iv, 8)
        key = n_string(key, 32)
        header_bytes = 50

        with open(filename, "rb") as picture:
            picture.seek(header_bytes)
            picture_content = picture.read()
            cipher = salsa_20_xor_bytes(picture_content, key, iv)
            with open(filename + ".encr", "wb") as encryption:
                picture.seek(0)
                encryption.write(picture.read(header_bytes))
                encryption.write(cipher)
        return True
    except Exception as e:
        return False


def decryption(iv: str, key: str, filename: str) -> bool:
    try:
        iv = n_string(iv, 8)
        key = n_string(key, 32)
        header_bytes = 50

        with open(filename + ".encr", "rb") as picture:
            picture.seek(header_bytes)
            encryption = picture.read()
            original = salsa_20_xor_bytes(encryption, key, iv)
            with open(filename, "wb") as decrypted:
                picture.seek(0)
                decrypted.write(picture.read(header_bytes))
                decrypted.write(original)

        return True
    except Exception as e:
        return False

print()
