import base64
from Crypto import Random
from Crypto.Cipher import AES


def encrypt(key, raw):
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return (base64.b64encode(iv + cipher.encrypt(raw)))


def decrypt(key, enc):
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return cipher.decrypt(enc[16:])
