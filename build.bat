:: All python modules from requirements.txt
:: must be installed in global python, not venv

pyinstaller --clean ^
  --noconsole ^
  --name "SecurePhotos"  ^
  --onefile src/__main__.py ^
  --add-data=src/;src/ ^
  --icon src/img/icon.ico ^
  --distpath . ^
  --hidden-import json ^
  --hidden-import ctypes ^
  --hidden-import webbrowser ^
  --hidden-import platform ^
  --hidden-import Crypto ^
  --hidden-import Crypto.Random ^
  --hidden-import Crypto.Hash.SHA256 ^
  --hidden-import Crypto.Cipher.AES ^
  --hidden-import PIL ^
  --hidden-import PIL.Image

IF EXIST build (rmdir /q /s build)
DEL SecurePhotos.spec