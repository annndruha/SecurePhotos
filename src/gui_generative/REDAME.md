# GUI

I am use the simplest way to make gui - QtCreator.

That's mean that `.ui` files with gui compile to `.py` file.
It's also means that not relevant to edit `.py` files in `gui_generative`, and py-files will have many linter errors.

**There are no linter in this folder. Don't add not-gui files here!**

* Install `pyuic5`
* Run `ui_to_py.bat` or `ui_to_py.sh`

### Second way

Without generation a py files, possible to load raw `.ui` files. Change lines in all gui from this:
```
self.ui = Ui_MainWindow()
self.ui.setupUi(self)
```
to this:
```
form, base = uic.loadUiType('gui/mainwindow.ui')
self.ui = form()
self.ui.setupUi(self)
```
