# hook-openpyxl.py
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = collect_submodules('openpyxl.cell')  # 自动收集子模块