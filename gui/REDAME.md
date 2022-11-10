# GUI

I am use the simplest way to make gui - QtCreator.

That's mean that `.ui` files with gui compile to `.py` file.
It's also means that not relevant to edit `.py` files in gui, and files will have many lints errors.

**There are no linter in this folder. Don't add not-gui files here!**

### After create venv:
* Activate venv (from this folder)
    ```commandline
    cd ../venv/Scripts
    activate
    cd ../../gui
    ```
* Run `ui_to_py.bat` or `ui_to_py.sh`