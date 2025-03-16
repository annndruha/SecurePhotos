import glob
import os
import shutil
import stat
import sys

from PIL import Image


def read_file(path: str) -> bytes:
    with open(path, 'rb') as f:
        return f.read()


def write_file(path: str, data: bytes) -> None:
    if os.path.exists(path):
        raise FileExistsError(path)
    with open(path, 'wb') as f:
        f.write(data)


def rotate_file_right(img_path: str):
    img = Image.open(img_path)
    img = img.rotate(-90, expand=True)
    img.save(img_path)


def rotate_file_left(img_path: str):
    img = Image.open(img_path)
    img = img.rotate(90, expand=True)
    img.save(img_path)


def make_dir_writable(function, path, exception):
    """The path on Windows cannot be gracefully removed due to being read-only,
    so we make the directory writable on a failure and retry the original function.
    """
    os.chmod(path, stat.S_IWRITE)
    function(path)


def get_folder_size(path: str) -> float:
    if not os.path.isdir(path):
        raise ValueError(f'Given path not a dir: {path}')
    res = 0
    files = glob.glob(os.path.join(path, '**'), recursive=True)
    for filepath in files:
        if os.path.isfile(filepath):
            res += os.path.getsize(filepath)
    return res


def size_to_text(size: int) -> str:
    for unit in ("B", "K", "M", "G", "T"):
        if size < 1024:
            break
        size /= 1024
    return f"{size:.1f}{unit}"


def delete_path(path: str):
    if path is None:
        return
    try:
        if os.path.isdir(path):
            shutil.rmtree(path, onerror=make_dir_writable)
        else:
            os.remove(path)
    except FileNotFoundError:
        pass


def copy_path(src_path: str, dest_path: str):
    if os.path.isdir(src_path):
        target_folder = str(os.path.join(dest_path, os.path.basename(src_path)))
        shutil.copytree(src_path, target_folder, dirs_exist_ok=True)
    else:
        shutil.copy(src_path, dest_path)


# https://stackoverflow.com/a/7675014/12627677
def resource_path(relative_path: str):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
