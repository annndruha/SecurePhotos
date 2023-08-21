import os
import stat
import argparse
import logging
import shutil

from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.Cipher import AES

from src.window_folderencrypt import FolderEncrypt, FolderDecrypt

CRYPT_EXTENSION = '.aes'
CRYPT_FOLDER_EXTENSION = '.aes_zip'
UTF_8 = 'utf-8'


class EmptyCipher(Exception):
    def __init__(self, *args, **kwargs):
        pass


class DecryptException(Exception):
    def __init__(self, *args, **kwargs):
        pass


class AESCipher:
    __hash: bytes
    __BS: int = 16

    def __init__(self, password: str):
        """
        Class stored SHA256 hash from keyphrase for encrypt and decrypt data.

        :param password: Password for encrypt
        """
        self.__hash = SHA256.new(bytes(password, 'utf-8')).digest()

    def hash(self):
        return str(self.__hash.hex())

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

        :param data: Data to be encrypted.
        :return: Encrypted data
        """
        data = self.__pad(data)
        iv = Random.new().read(AES.block_size)
        aes = AES.new(self.__hash, AES.MODE_CBC, iv)
        return iv + aes.encrypt(data)

    def decrypt(self, data: bytes) -> bytes:
        """
        AES-256 decrypt data with hash stored in this class.

        :param data: Data to be decrypted.
        :return: Decrypted data
        """
        try:
            iv = data[:AES.block_size]
            aes = AES.new(self.__hash, AES.MODE_CBC, iv)
            return self.__unpad(aes.decrypt(data[AES.block_size:]))
        except ValueError:
            raise DecryptException


def read_file(path: str) -> bytes:
    with open(path, 'rb') as f:
        byte = f.read()
        return byte


def write_file(path: str, data: bytes) -> None:
    with open(path, 'wb') as f:
        f.write(data)


def encrypt_file(path: str, cipher: AESCipher, delete_original=False) -> None:
    if cipher is None:
        raise EmptyCipher
    file_bytes = read_file(path)
    encrypted_text = cipher.encrypt(file_bytes)
    aes_path = path + CRYPT_EXTENSION
    # TODO: Raise if file exist
    write_file(aes_path, encrypted_text)

    if delete_original:
        delete_path(path)


def decrypt_file(path: str, cipher: AESCipher, delete_original=False) -> None:
    if cipher is None:
        raise EmptyCipher
    file_bytes = read_file(path)
    decrypted_text = cipher.decrypt(file_bytes)
    orig_path = os.path.splitext(path)[0]
    # TODO: Raise if file exist
    write_file(orig_path, decrypted_text)

    if delete_original:
        delete_path(path)


def decrypt_runtime(path: str, cipher: AESCipher):
    if cipher is None:
        raise EmptyCipher
    else:
        file_bytes = read_file(path)
        decrypted_text = cipher.decrypt(file_bytes)
        return decrypted_text


def encrypt_folder(ui_object: FolderEncrypt,
                   encrypt_type: str,
                   folder_path: str,
                   cipher: AESCipher,
                   delete_original=False) -> None:
    match encrypt_type:
        case 'one':
            # TODO: Raise if file exist
            shutil.make_archive(folder_path, 'zip', folder_path)
            encrypt_file(folder_path + '.zip', cipher, delete_original=delete_original)
            os.rename(folder_path + '.zip' + CRYPT_EXTENSION, folder_path + CRYPT_FOLDER_EXTENSION)
            delete_path(folder_path)

        case 'files':
            i, cnt_files = 0, sum([len(files) for r, d, files in os.walk(folder_path)])
            for path, _, files in os.walk(folder_path):
                for name in files:
                    filepath = os.path.join(path, name)
                    ext = os.path.splitext(filepath)[1]
                    if ext != CRYPT_EXTENSION:
                        encrypt_file(filepath, cipher, delete_original=delete_original)
                    i += 1
                    ui_object.set_progress_bar_value(int(i * 100 / cnt_files))
        case _:
            pass


def decrypt_folder(ui_object: FolderDecrypt,
                   folder_path: str,
                   cipher: AESCipher,
                   delete_original=False) -> None:
    i, cnt_files = 0, sum([len(files) for r, d, files in os.walk(folder_path)])
    for path, _, files in os.walk(folder_path):
        for name in files:
            filepath = os.path.join(path, name)
            ext = os.path.splitext(filepath)[1]
            if ext == CRYPT_EXTENSION:
                decrypt_file(filepath, cipher, delete_original=delete_original)
            i += 1
            ui_object.set_progress_bar_value(int(i * 100 / cnt_files))


def decrypt_folder_file(path: str, cipher: AESCipher, delete_original=False) -> None:
    # TODO: Raise if file exist
    path_zipped_aes = path.replace(CRYPT_FOLDER_EXTENSION, '.zip' + CRYPT_EXTENSION)
    os.rename(path, path_zipped_aes)
    decrypt_file(path_zipped_aes, cipher, delete_original=delete_original)

    path_zipped = path.replace(CRYPT_FOLDER_EXTENSION, '.zip')
    shutil.unpack_archive(path_zipped, extract_dir=path.replace(CRYPT_FOLDER_EXTENSION, ''))
    delete_path(path_zipped)


def make_dir_writable(function, path, exception):
    """The path on Windows cannot be gracefully removed due to being read-only,
    so we make the directory writable on a failure and retry the original function.
    """
    os.chmod(path, stat.S_IWRITE)
    function(path)


def delete_path(path):
    try:
        if os.path.isdir(path):
            shutil.rmtree(path, onerror=make_dir_writable)
        else:
            os.remove(path)
    except FileNotFoundError:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encrypt files with console. Usage:"
                                                 "\n python aes.py -e -f test.jpg -p mypassword")
    parser.add_argument("-e", action="store_true", help="Encrypt mode")
    parser.add_argument("-d", action="store_true", help="Decrypt mode")
    parser.add_argument("-f", default=None, help="Path to file to encrypt/decrypt")
    parser.add_argument("-p", default=None, help="""Password for encrypt/decrypt. Password -> sha256 -> aes256 key""")

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
