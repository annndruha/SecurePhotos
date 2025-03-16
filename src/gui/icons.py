from PyQt5.QtGui import QIcon, QImageReader, QPixmap

from src.utils.utils import resource_path as rp


class Icons:
    """Store all icons in RAM for fast rendering in FilesTree etc."""
    favicon = QIcon(rp('src/img/icon.svg'))
    folder_open = QIcon(rp('src/img/icons/folder_open.svg'))
    settings = QIcon(rp('src/img/icons/settings.svg'))
    rotate_left = QIcon(rp('src/img/icons/rotate_left.svg'))
    rotate_right = QIcon(rp('src/img/icons/rotate_right.svg'))
    delete = QIcon(rp('src/img/icons/delete.svg'))
    zoom_none = QIcon(rp('src/img/icons/zoom_none.svg'))
    open_full = QIcon(rp('src/img/icons/open_full.svg'))
    key = QIcon(rp('src/img/icons/key.svg'))
    lock = QIcon(rp('src/img/icons/lock.svg'))
    folder_lock_open = QIcon(rp('src/img/icons/folder_lock_open.svg'))
    close_full = QIcon(rp('src/img/icons/close_full.svg'))
    zoom_in = QIcon(rp('src/img/icons/zoom_in.svg'))
    zoom_out = QIcon(rp('src/img/icons/zoom_out.svg'))
    not_locked = QIcon(rp('src/img/icons/not_locked.svg'))
    folder_lock = QIcon(rp('src/img/icons/folder_lock.svg'))
    lock_open = QIcon(rp('src/img/icons/lock_open.svg'))
    image = QIcon(rp("src/img/icons/image.svg"))
    movie = QIcon(rp("src/img/icons/movie.svg"))
    file_zip = QIcon(rp("src/img/icons/file_zip.svg"))
    folder = QIcon(rp("src/img/icons/folder.svg"))
    folder.addFile(rp("src/img/icons/folder_open.svg"), state=folder.On)
    copy = QIcon(rp("src/img/icons/copy.svg"))
    open = QIcon(rp("src/img/icons/open_in.svg"))


class Placeholders:
    """
    Placeholders images
    """
    def __init__(self):
        self.try_another_key = QPixmap.fromImage(QImageReader(rp('src/img/placeholders/try_another_key.png')).read())
        self.broken_image = QPixmap.fromImage(QImageReader(rp('src/img/placeholders/broken_image.png')).read())
        self.encrypted = QPixmap.fromImage(QImageReader(rp('src/img/placeholders/encrypted.png')).read())
        self.video = QPixmap.fromImage(QImageReader(rp('src/img/placeholders/video.png')).read())
        self.nothing_to_show = QPixmap.fromImage(QImageReader(rp('src/img/placeholders/nothing_to_show.png')).read())
