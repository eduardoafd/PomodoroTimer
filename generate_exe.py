import os
import shutil
import PyInstaller.__main__

if os.path.exists('./pomodoro.exe'):
    os.remove('./pomodoro.exe')

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--noconsole',
    '--name=pomodoro',
    '--noconfirm',
    '--clean',
    '--icon=./assets/tomato.ico'
])

# Move the executable to the root directory
shutil.move('./dist/pomodoro.exe', './pomodoro.exe')

# Clean up the dist and build directories
shutil.rmtree('./dist')
shutil.rmtree('./build')
os.remove('./pomodoro.spec')
