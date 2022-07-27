import os
import shutil
from PIL import Image


def rotate_file_right(img_path):
    print('rotate right')
    img = Image.open(img_path)
    # with Image.open(img_path) as img:
    print(img)
    img = img.rotate(-90, expand=1)
    print(img)
    img.save(img_path)


def rotate_file_left(img_path):
    print('rotate left')
    img = Image.open(img_path)
    # with Image.open(img_path) as img:
    img = img.rotate(90, expand=1)
    img.save(img_path)


def delete_path(path):
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    except FileNotFoundError:
        pass
