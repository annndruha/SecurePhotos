# GUI

We use the simplest way to make gui - QtCreator.

That's mean that `.ui` files with gui compile to `.py` file.
It's also means that not relevant to edit `.py` files in gui, and files will have many lints errors.

**There are no linter in this folder. Don't add not-gui files here!**

### Compile `.ui` to `.py`
* Just run `mainwindow_ui_to_py.bat` and `enterkey_ui_to_py.bat`
* or ```pyuic5 guifile.ui -o pythonfile.py```