import os
import argparse
import logging

from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.Cipher import AES

ENCODED_EXTENSION = '.aes'
UTF_8 = 'utf-8'


class AESCipher:
    __hash: bytes
    __BS: int = 16

    def __init__(self, password: str):
        """
        Class stored SHA256 hash from keyphrase for encrypt and decrypt data.

        :param password: Password for encrypt
        """
        self.__hash = SHA256.new(bytes(password, 'utf-8')).digest()

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


def read_file(path: str) -> bytes:
    with open(path, 'rb') as f:
        byte = f.read()
        return byte


def write_file(path: str, data: bytes) -> None:
    with open(path, 'wb') as f:
        f.write(data)


def encrypt_file(path: str, key: str) -> None:
    file_bytes = read_file(path)
    cipher = AESCipher(key)
    encrypted_text = cipher.encrypt(file_bytes)
    path += ENCODED_EXTENSION
    write_file(path, encrypted_text)


def decrypt_file(path: str, key: str) -> None:
    file_bytes = read_file(path)
    cipher = AESCipher(key)
    decrypted_text = cipher.decrypt(file_bytes)
    path = os.path.splitext(path)[0]
    write_file(path, decrypted_text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encrypt files with console. Usage:"
                                                 "\n python aes.py -e -f test.jpg -p mypassword")
    parser.add_argument("-e", action="store_true", help="Encrypt mode")
    parser.add_argument("-d", action="store_true", help="Decrypt mode")
    parser.add_argument("-f", default=None, help="Path to file to encrypt/decrypt")
    parser.add_argument("-p", default=None, help="""Password for encrypt/decrypt. Password -> sha256 -> 
    aes256 key""")

    args = parser.parse_args()
    if bool(args.e) != bool(args.d):
        pass
        if args.f is not None and args.p is not None:
            if args.e is True:
                encrypt_file(args.f, args.p)
            else:
                decrypt_file(args.f, args.p)
        else:
            logging.error('File path "-f" or password "-p" not specified.')
    else:
        logging.error('Unknown mode, use "-e" or "-d" for encrypt or decrypt respectively.')

