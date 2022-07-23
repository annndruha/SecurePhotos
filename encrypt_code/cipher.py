import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random


class AESCipher:
    key: bytes
    __BS: int = 16

    def __init__(self, keyphrase: str):
        self.key = bytes.fromhex(hashlib.sha256(keyphrase.encode('utf-8')).hexdigest())

    def __pad(self, s: bytes) -> bytes:
        pad_len = self.__BS - len(s) % self.__BS
        return s + pad_len * chr(pad_len).encode()

    @staticmethod
    def __unpad(s):
        return s[:-ord(s[len(s) - 1:])]

    def encrypt(self, data: bytes) -> bytes:
        data = self.__pad(data)
        iv = Random.new().read(AES.block_size)
        aes = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + aes.encrypt(data))

    def decrypt(self, enc: bytes) -> bytes:
        enc = base64.b64decode(enc)
        iv = enc[:16]
        aes = AES.new(self.key, AES.MODE_CBC, iv)
        return self.__unpad(aes.decrypt(enc[16:]))
