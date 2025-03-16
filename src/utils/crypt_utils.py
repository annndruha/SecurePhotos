import glob
import os
import shutil

from src.gui.window_progressbar import ProgressBarDialog
from src.gui.window_progressbar_onefile import ProgressBarOneFileDialog
from src.utils.aes import AESCipher
from src.utils.utils import delete_path, get_folder_size, read_file, write_file

CRYPT_EXTENSION = '.aes'
CRYPT_FOLDER_EXTENSION = '.aes_zip'


class EmptyCipher(Exception):
    pass


def encrypt_file(path: str,
                 cipher: AESCipher,
                 delete_original=False) -> None:
    if cipher is None:
        raise EmptyCipher
    file_bytes = read_file(path)
    encrypted_text = cipher.encrypt(file_bytes)
    aes_path = path + CRYPT_EXTENSION
    write_file(aes_path, encrypted_text)

    if delete_original:
        delete_path(path)


def decrypt_file(path: str,
                 cipher: AESCipher,
                 delete_original=False) -> None:
    """Decrypt file, save decrypted on disk, remove encrypted if set"""
    if cipher is None:
        raise EmptyCipher
    file_bytes = read_file(path)
    decrypted_text = cipher.decrypt(file_bytes)
    orig_path = os.path.splitext(path)[0]
    write_file(orig_path, decrypted_text)

    if delete_original:
        delete_path(path)


def decrypt_runtime(path: str,
                    cipher: AESCipher):
    """Try to decrypt folder in runtime, without write decrypted on disk"""
    if cipher is None:
        raise EmptyCipher
    else:
        file_bytes = read_file(path)
        decrypted_text = cipher.decrypt(file_bytes)
        return decrypted_text


def encrypt_folder_each_file(path: str,
                             cipher: AESCipher,
                             progress: ProgressBarDialog,
                             delete_original=False) -> None:
    """Encrypt each file in folder separately"""
    if cipher is None:
        raise EmptyCipher
    files = glob.glob(os.path.join(path, '**'), recursive=True)
    for i, filepath in enumerate(files):
        progress.set_state(int(i * 100 / len(files)), filepath)
        if progress.was_canceled():
            break
        if os.path.isfile(filepath) and os.path.splitext(filepath)[1] != CRYPT_EXTENSION:
            encrypt_file(filepath, cipher, delete_original=delete_original)
    progress.set_state(100, 'Done')


def encrypt_folder_to_one_file(path: str,
                               cipher: AESCipher,
                               progress_onefile: ProgressBarOneFileDialog,
                               delete_original=False) -> None:
    """Encrypt whole folder to one file"""
    if cipher is None:
        raise EmptyCipher
    if os.path.exists(path + '.zip'):
        raise FileExistsError(path + '.zip')
    if os.path.exists(path + '.zip' + CRYPT_EXTENSION):
        raise FileExistsError(path + '.zip' + CRYPT_EXTENSION)
    if os.path.exists(path + CRYPT_FOLDER_EXTENSION):
        raise FileExistsError(path + CRYPT_FOLDER_EXTENSION)

    progress_onefile.set_state('calc_size')
    size = get_folder_size(path)

    progress_onefile.set_state('archiving', size=size)
    shutil.make_archive(path, 'zip', path)
    if progress_onefile.was_canceled():
        delete_path(path + '.zip')
        return

    progress_onefile.set_state('encrypting')
    encrypt_file(path + '.zip', cipher, delete_original=delete_original)
    if progress_onefile.was_canceled():
        delete_path(path + '.zip' + CRYPT_EXTENSION)
        return

    progress_onefile.set_state('deleting')
    os.rename(path + '.zip' + CRYPT_EXTENSION, path + CRYPT_FOLDER_EXTENSION)
    delete_path(path)

    progress_onefile.set_state('done')


def decrypt_folder_file(path: str,
                        cipher: AESCipher,
                        delete_original=False) -> None:
    """Decrypt folder as one-file archive"""
    if cipher is None:
        raise EmptyCipher
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
    """
    Decrypt folder file by file. Update progress bar
    """
    if cipher is None:
        raise EmptyCipher
    files = glob.glob(os.path.join(path, '**'), recursive=True)
    for i, filepath in enumerate(files):
        progress.set_state(int(i * 100 / len(files)), filepath)
        if progress.was_canceled():
            break
        if os.path.isfile(filepath) and os.path.splitext(filepath)[1] == CRYPT_EXTENSION:
            decrypt_file(filepath, cipher, delete_original=delete_original)
    progress.set_state(100, 'Done')
