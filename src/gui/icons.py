from PyQt5.QtGui import QIcon, QImageReader, QPixmap

from src.utils.utils import resource_path as rp


class Icons:
    """Store all icons in RAM for fast rendering in FilesTree etc."""
    def __init__(self):
        self.favicon = QIcon(rp('src/img/icon.svg'))
        self.folder_open = QIcon(rp('src/img/icons/folder_open.svg'))
        self.settings = QIcon(rp('src/img/icons/settings.svg'))
        self.rotate_left = QIcon(rp('src/img/icons/rotate_left.svg'))
        self.rotate_right = QIcon(rp('src/img/icons/rotate_right.svg'))
        self.delete = QIcon(rp('src/img/icons/delete.svg'))
        self.zoom_none = QIcon(rp('src/img/icons/zoom_none.svg'))
        self.open_full = QIcon(rp('src/img/icons/open_full.svg'))
        self.key = QIcon(rp('src/img/icons/key.svg'))
        self.lock = QIcon(rp('src/img/icons/lock.svg'))
        self.folder_lock_open = QIcon(rp('src/img/icons/folder_lock_open.svg'))
        self.close_full = QIcon(rp('src/img/icons/close_full.svg'))
        self.open_full = QIcon(rp('src/img/icons/open_full.svg'))
        self.zoom_in = QIcon(rp('src/img/icons/zoom_in.svg'))
        self.zoom_out = QIcon(rp('src/img/icons/zoom_out.svg'))
        self.zoom_none = QIcon(rp('src/img/icons/zoom_none.svg'))
        self.not_locked = QIcon(rp('src/img/icons/not_locked.svg'))
        self.folder_lock = QIcon(rp('src/img/icons/folder_lock.svg'))
        self.lock_open = QIcon(rp('src/img/icons/lock_open.svg'))
        self.image = QIcon(rp("src/img/icons/image.svg"))
        self.movie = QIcon(rp("src/img/icons/movie.svg"))
        self.file_zip = QIcon(rp("src/img/icons/file_zip.svg"))
        self.folder = QIcon(rp("src/img/icons/folder.svg"))
        self.folder.addFile(rp("src/img/icons/folder_open.svg"), state=self.folder.On)
        self.copy = QIcon(rp("src/img/icons/copy.svg"))
        self.open = QIcon(rp("src/img/icons/open_in.svg"))


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
