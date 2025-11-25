# -*- mode: python ; coding: utf-8 -*-
import os
import sys
import glob
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

block_cipher = None

# Collect GLFW dynamic libraries
glfw_binaries = collect_dynamic_libs('glfw')

# Manual fallback: try to find GLFW DLL in site-packages
if not glfw_binaries:
    try:
        import glfw
        glfw_path = os.path.dirname(glfw.__file__)
        # Look for DLL files in glfw directory
        for dll_pattern in ['*.dll', 'glfw*.dll', 'libglfw*.dll']:
            dll_files = glob.glob(os.path.join(glfw_path, dll_pattern))
            for dll_file in dll_files:
                glfw_binaries.append((dll_file, '.'))
        # Also check in subdirectories
        for root, dirs, files in os.walk(glfw_path):
            for dll_pattern in ['*.dll', 'glfw*.dll', 'libglfw*.dll']:
                dll_files = glob.glob(os.path.join(root, dll_pattern))
                for dll_file in dll_files:
                    rel_path = os.path.relpath(os.path.dirname(dll_file), glfw_path)
                    glfw_binaries.append((dll_file, rel_path if rel_path != '.' else '.'))
    except ImportError:
        pass

# Collect data files for glfw if any
glfw_datas = collect_data_files('glfw', includes=['*.dll'])

# Add other data files
datas = [
    ('exemple_textures', 'exemple_textures'),
    ('engine3d/engine-icon.png', 'engine3d'),
]

# If glfw_datas has entries, add them
if glfw_datas:
    datas.extend(glfw_datas)

a = Analysis(
    ['example.py'],
    pathex=[os.getcwd()],  # Include current directory so config.py can be found
    binaries=glfw_binaries,  # Include GLFW DLLs
    datas=datas,
    hiddenimports=[
        'config',  # Required for dynamic import in core.py
        'glfw',
        'glfw.library',
        'OpenGL',
        'OpenGL.GL',
        'OpenGL.GLU',
        'imgui',
        'imgui.integrations.glfw',
        'pygame',
        'numpy',
        'PIL',
        'PIL._imagingtk',
        'PIL._tkinter_finder',
    ],
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=['hooks/rthook_glfw.py'],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='build',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='engine3d/engine-icon.png' if os.path.exists('engine3d/engine-icon.png') else None,
)

