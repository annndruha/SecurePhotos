import os
import sys
import stat
import shutil
import glob

from PIL import Image


def rotate_file_right(img_path):
    img = Image.open(img_path)
    img = img.rotate(-90, expand=True)
    img.save(img_path)


def rotate_file_left(img_path):
    img = Image.open(img_path)
    img = img.rotate(90, expand=True)
    img.save(img_path)


def make_dir_writable(function, path, exception):
    """The path on Windows cannot be gracefully removed due to being read-only,
    so we make the directory writable on a failure and retry the original function.
    """
    os.chmod(path, stat.S_IWRITE)
    function(path)


def get_folder_size(path) -> float:
    if not os.path.isdir(path):
        raise ValueError(f'Given path not a dir: {path}')
    res = 0
    files = glob.glob(os.path.join(path, '**'), recursive=True)
    for filepath in files:
        if os.path.isfile(filepath):
            res += os.path.getsize(filepath)
    return res


def size_to_text(size):
    for unit in ("B", "K", "M", "G", "T"):
        if size < 1024:
            break
        size /= 1024
    return f"{size:.1f}{unit}"


def delete_path(path):
    if path is None:
        return
    try:
        if os.path.isdir(path):
            shutil.rmtree(path, onerror=make_dir_writable)
        else:
            os.remove(path)
    except FileNotFoundError:
        pass


# https://stackoverflow.com/a/7675014/12627677
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
