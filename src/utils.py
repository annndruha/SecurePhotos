import os
import shutil
from PIL import Image


def rotate_file_right(img_path):
    img = Image.open(img_path)
    img = img.rotate(-90, expand=True)
    img.save(img_path)


def rotate_file_left(img_path):
    img = Image.open(img_path)
    img = img.rotate(90, expand=True)
    img.save(img_path)


def delete_path(path):
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    except FileNotFoundError:
        pass
