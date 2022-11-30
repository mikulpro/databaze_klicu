import hashlib


def hash_func(text):
    encoded_str = text.encode()
    hash512 = hashlib.sha512(encoded_str).hexdigest()
    return hash512
