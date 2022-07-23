from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.Cipher import AES


class AESCipher:
    __hash: bytes
    __BS: int = 16

    def __init__(self, keyphrase: str):
        """
        Class stored SHA256 hash from keyphrase for encrypt and decrypt data.

        :param keyphrase: Password for encrypt
        """
        self.__hash = SHA256.new(bytes(keyphrase, 'utf-8')).digest()

    def __pad(self, data: bytes) -> bytes:
        """
        Padding data for correct AES encrypt

        :param data: Data for encrypt
        :return: Padded data
        """
        pad_len = self.__BS - len(data) % self.__BS
        return data + pad_len * chr(pad_len).encode()

    @staticmethod
    def __unpad(data):
        """
        Remove padding from data

        :param data: Data with padding
        :return: Unpadded data
        """
        return data[:-ord(data[len(data) - 1:])]

    def encrypt(self, data: bytes) -> bytes:
        """
        AES-256 encrypt data with hash stored in this class

        :param data: Data to be encrypted
        :return: Encrypted data
        """
        data = self.__pad(data)
        iv = Random.new().read(AES.block_size)
        aes = AES.new(self.__hash, AES.MODE_CBC, iv)
        return iv + aes.encrypt(data)

    def decrypt(self, data: bytes) -> bytes:
        """
        AES-256 decrypt data with hash stored in this class.

        :param data: Data to be decrypted
        :return: Decrypted data
        """
        iv = data[:AES.block_size]
        aes = AES.new(self.__hash, AES.MODE_CBC, iv)
        return self.__unpad(aes.decrypt(data[AES.block_size:]))
