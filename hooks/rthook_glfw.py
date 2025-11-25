"""
Runtime hook for glfw library and module path setup
Ensures GLFW DLL can be found at runtime in PyInstaller bundle
Also ensures that modules like 'config' can be found
"""
import os
import sys

# Add PyInstaller's temporary directory to DLL search path and Python path
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    base_path = sys._MEIPASS
    
    # Add base path to Python path so modules like 'config' can be found
    if base_path not in sys.path:
        sys.path.insert(0, base_path)
    
    # Add base path to PATH so Windows can find DLLs
    os.environ['PATH'] = base_path + os.pathsep + os.environ.get('PATH', '')
    
    # Also try to add any glfw subdirectory
    glfw_paths = [
        base_path,
        os.path.join(base_path, 'glfw'),
        os.path.join(base_path, 'lib'),
    ]
    
    for path in glfw_paths:
        if os.path.exists(path):
            if path not in os.environ.get('PATH', ''):
                os.environ['PATH'] = path + os.pathsep + os.environ.get('PATH', '')

