@echo off
setlocal

echo ==============================
echo Building dxtools.dll ...
echo ==============================

REM --- Find Visual Studio compiler ---
call "%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe" ^
  -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 ^
  -property installationPath > "%temp%\vs_path.txt"

set /p VS_PATH=<"%temp%\vs_path.txt"

if "%VS_PATH%"=="" (
    echo ERROR: Visual Studio Build Tools not found.
    echo Install: "Build Tools for Visual Studio" with C++ tools.
    exit /b 1
)

echo VS found at: %VS_PATH%

call "%VS_PATH%\VC\Auxiliary\Build\vcvars64.bat"

REM --- Compile the DLL ---
cl /LD /EHsc ^
  source\directx\dx9tools.cpp ^
  /Fe:source\directx\dxtools.dll ^
  /link d3d9.lib user32.lib gdi32.lib

if %errorlevel% neq 0 (
    echo Build FAILED.
    exit /b 1
)

echo.
echo ==============================
echo Build SUCCESS: dxtools.dll
echo ==============================
echo.

