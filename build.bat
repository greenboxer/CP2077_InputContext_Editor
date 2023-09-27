rem CP2077 InputContext Editor Requires: Python 3.8

pyinstaller --noconsole --noconfirm --clean cpxmleditor.py


if not exist "build" mkdir build
if exist "build\CP2077_InputContext_Editor" rmdir /s /q builds\CP2077_InputContext_Editor

move /y .\dist\cpxmleditor .\dist\CP2077_InputContext_Editor
rmdir /s /q build

cd dist
tar -czf CP2077_InputContext_Editor.tar.gz cpxmleditor

rmdir /s /q main
rmdir /s /q CP2077_InputContext_Editor