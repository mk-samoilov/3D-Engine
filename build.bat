@echo off
echo Building 3D Engine executable...
echo.

REM Clean previous build
if exist "build" (
    echo Cleaning previous build...
    rmdir /s /q build
)

if exist "dist" (
    echo Cleaning previous dist...
    rmdir /s /q dist
)

REM Build using the spec file
echo Running PyInstaller...
pyinstaller build_example.spec --clean

REM Copy the executable to build directory
if exist "dist\build.exe" (
    echo.
    echo Copying executable to build directory...
    if not exist "build" mkdir build
    copy dist\build.exe build\build.exe
    
    REM Copy data directories
    if exist "exemple_textures" (
        xcopy /E /I /Y exemple_textures build\exemple_textures
    )
    if exist "engine3d\engine-icon.png" (
        if not exist "build\engine3d" mkdir build\engine3d
        copy engine3d\engine-icon.png build\engine3d\engine-icon.png
    )
    
    echo.
    echo Build completed successfully!
    echo Executable is at: build\build.exe
) else (
    echo.
    echo ERROR: Build failed! Check the output above for errors.
    exit /b 1
)

