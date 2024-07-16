import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "excludes": [
        "PySide6", "unittest", "sqlite3", "numpy", "matplotlib", "zstandard",
        "oead", "evfl", "keystone-engine", "PyYAML", "quick-tex", "Pillow",
        "sys", "os"
    ],
    "zip_include_packages": ["encodings", "tkinter"],
    "include_files": ["customize.txt", "README.txt"],
    "optimize": 2}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "Basic No-Hit Tracker",
    version = "0.1",
    description = "An extremely basic No-Hit Tracker",
    options = {"build_exe": build_exe_options},
    executables = [Executable("main.py", base=base, target_name="Basic No-Hit Tracker")]
)