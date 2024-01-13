import glob
import os
import stat
import argparse
import logging
import shutil

from src.aes import AESCipher
from src.window_progressbar import ProgressBarDialog

CRYPT_EXTENSION = '.aes'
CRYPT_FOLDER_EXTENSION = '.aes_zip'
UTF_8 = 'utf-8'


class EmptyCipher(Exception):
    pass


def read_file(path: str) -> bytes:
    with open(path, 'rb') as f:
        byte = f.read()
        return byte


def write_file(path: str, data: bytes) -> None:
    if os.path.exists(path):
        raise FileExistsError(path)
    with open(path, 'wb') as f:
        f.write(data)


def encrypt_file(path: str, cipher: AESCipher, delete_original=False) -> None:
    if cipher is None:
        raise EmptyCipher
    file_bytes = read_file(path)
    encrypted_text = cipher.encrypt(file_bytes)
    aes_path = path + CRYPT_EXTENSION
    write_file(aes_path, encrypted_text)

    if delete_original:
        delete_path(path)


def decrypt_file(path: str, cipher: AESCipher, delete_original=False) -> None:
    if cipher is None:
        raise EmptyCipher
    file_bytes = read_file(path)
    decrypted_text = cipher.decrypt(file_bytes)
    orig_path = os.path.splitext(path)[0]
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


def encrypt_folder(encrypt_type: str,
                   path: str,
                   cipher: AESCipher,
                   progress: ProgressBarDialog,
                   delete_original=False) -> None:
    match encrypt_type:
        case 'one':
            if os.path.exists(path + '.zip'):
                raise FileExistsError(path + '.zip')
            if os.path.exists(path + '.zip' + CRYPT_EXTENSION):
                raise FileExistsError(path + '.zip' + CRYPT_EXTENSION)
            if os.path.exists(path + CRYPT_FOLDER_EXTENSION):
                raise FileExistsError(path + CRYPT_FOLDER_EXTENSION)

            shutil.make_archive(path, 'zip', path)
            encrypt_file(path + '.zip', cipher, delete_original=delete_original)
            os.rename(path + '.zip' + CRYPT_EXTENSION, path + CRYPT_FOLDER_EXTENSION)
            delete_path(path)

        case 'files':
            files = glob.glob(os.path.join(path, '*'), recursive=True)
            for i, filepath in enumerate(files):
                progress.set_state(int(i * 100 / len(files)), filepath)
                if progress.was_canceled():
                    break
                if os.path.isfile(filepath) and os.path.splitext(filepath)[1] != CRYPT_EXTENSION:
                    encrypt_file(filepath, cipher, delete_original=delete_original)
            progress.set_state(100, 'Done')
        case _:
            pass


def decrypt_folder_file(path: str, cipher: AESCipher, delete_original=False) -> None:
    temp_zip_aes = path.replace(CRYPT_FOLDER_EXTENSION, '.zip' + CRYPT_EXTENSION)
    temp_zip = path.replace(CRYPT_FOLDER_EXTENSION, '.zip')
    out_path = path.replace(CRYPT_FOLDER_EXTENSION, '')
    if os.path.exists(out_path):
        raise FileExistsError(out_path)
    if os.path.exists(temp_zip):
        raise FileExistsError(temp_zip)
    if os.path.exists(temp_zip_aes):
        raise FileExistsError(temp_zip_aes)

    os.rename(path, temp_zip_aes)
    decrypt_file(temp_zip_aes, cipher, delete_original=delete_original)

    shutil.unpack_archive(temp_zip, extract_dir=out_path)
    delete_path(temp_zip)


def decrypt_folder(path: str,
                   cipher: AESCipher,
                   progress: ProgressBarDialog,
                   delete_original=False) -> None:
    files = glob.glob(os.path.join(path, '*'), recursive=True)
    for i, filepath in enumerate(files):
        progress.set_state(int(i * 100 / len(files)), filepath)
        if progress.was_canceled():
            break
        if os.path.isfile(filepath) and os.path.splitext(filepath)[1] == CRYPT_EXTENSION:
            decrypt_file(filepath, cipher, delete_original=delete_original)
    progress.set_state(100, 'Done')


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
