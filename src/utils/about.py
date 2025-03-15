import sys

import Crypto
import PIL

from PyQt5.QtCore import PYQT_VERSION_STR, QT_VERSION_STR

from src.version import __version__


class About:
    def __init__(self):
        self.__version__ = __version__
        self._python_version = sys.version.split('(')[0] if '(' in sys.version else sys.version

    @property
    def info(self):
        return f"""
                SecurePhotos: <a href="https://github.com/annndruha/SecurePhotos/releases">{__version__}</a>
                <p>
                <a href="https://github.com/annndruha/SecurePhotos">Source code</a>
                <p>
                Autor: <a href="https://github.com/annndruha">@annndruha</a>
                <p>
                <h4>
                <a href="https://github.com/annndruha/SecurePhotos/issues">Report problem</a>
                </h4>
                <hr>
                """

    @property
    def versions(self):
        versions_list = [
            f'SecurePhotos: {__version__}',
            f'Python: {self._python_version}',
            f'Crypto: {Crypto.__version__}',
            f'PIL: {PIL.__version__}',
            f'Qt: {QT_VERSION_STR}',
            f'PyQt5: {PYQT_VERSION_STR}'
        ]
        return versions_list

    @property
    def system_info(self):
        return '<p>'.join(self.versions)

    @property
    def system_info_clipboard(self):
        return '\n'.join(self.versions)
