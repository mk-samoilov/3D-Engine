"""
PyInstaller hook for glfw library
This ensures GLFW DLL files are included in the build
"""
from PyInstaller.utils.hooks import collect_dynamic_libs, collect_data_files
import os
import glob

# Collect all dynamic libraries (DLLs) from glfw package
binaries = collect_dynamic_libs('glfw')

# Also try to find DLLs manually if collect_dynamic_libs didn't find them
if not binaries:
    try:
        import glfw
        glfw_path = os.path.dirname(glfw.__file__)
        
        # Common DLL names for GLFW
        dll_names = ['glfw3.dll', 'libglfw3.dll', 'glfw.dll', 'libglfw.dll']
        
        # Check in glfw package directory
        for dll_name in dll_names:
            dll_path = os.path.join(glfw_path, dll_name)
            if os.path.exists(dll_path):
                binaries.append((dll_path, '.'))
        
        # Also search for any DLL files
        for dll_file in glob.glob(os.path.join(glfw_path, '*.dll')):
            binaries.append((dll_file, '.'))
        
        # Check subdirectories
        for root, dirs, files in os.walk(glfw_path):
            for dll_file in glob.glob(os.path.join(root, '*.dll')):
                rel_dir = os.path.relpath(root, glfw_path)
                target_dir = rel_dir if rel_dir != '.' else '.'
                binaries.append((dll_file, target_dir))
    except ImportError:
        pass

# Collect any data files
datas = collect_data_files('glfw', includes=['*.dll'])

