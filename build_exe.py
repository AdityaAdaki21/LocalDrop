import PyInstaller.__main__
import os
import platform

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Use correct path separator based on OS
separator = ';' if platform.system() == 'Windows' else ':'

PyInstaller.__main__.run([
    'LocalDrop.py',
    '--onefile',
    '--add-data', f'{os.path.join(current_dir, "index.html")}{separator}.',
    '--console',
    '--name', 'LocalDrop',
]) 