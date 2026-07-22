# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import (
    collect_data_files,
    collect_submodules,
)

block_cipher = None

hiddenimports = (
    collect_submodules("PySide6")
    + collect_submodules("fitz")
    + collect_submodules("pymupdf")
    + collect_submodules("rapidocr_onnxruntime")
    + collect_submodules("docling")
    + collect_submodules("tiktoken")
)

datas = [
    ("assets", "assets"),
]

datas += collect_data_files(
    "docling",
)

datas += collect_data_files(
    "rapidocr_onnxruntime",
)

a = Analysis(
    ["src/athena/main.py"],
    pathex=["src"],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "pytest",
        "mypy",
        "ruff",
        "tests",
    ],
    noarchive=False,
)

pyz = PYZ(
    a.pure,
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Athena",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="Athena",
)