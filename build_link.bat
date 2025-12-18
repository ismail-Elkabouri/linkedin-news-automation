@echo off
REM LINK App Build Script - Creates LINK.exe standalone executable
REM This script builds the LINK.exe file that users can download

echo.
echo ============================================
echo   LINK App - Building Executable
echo ============================================
echo.

REM Clean previous builds
echo Cleaning previous builds...
rmdir /s /q dist build 2>nul
del LINK.spec 2>nul

REM Build with PyInstaller
echo.
echo Building LINK.exe... (this takes 1-2 minutes)
echo.

pyinstaller ^
  --onefile ^
  --windowed ^
  --name=LINK ^
  --hidden-import=PyQt5 ^
  --hidden-import=PyQt5.QtWidgets ^
  --hidden-import=PyQt5.QtCore ^
  --hidden-import=PyQt5.QtGui ^
  --distpath=dist ^
  --workpath=build ^
  --specpath=build ^
  gui_app.py

if exist "dist\LINK.exe" (
  echo.
  echo ✓ SUCCESS! LINK.exe created!
  echo.
  for /F "tokens=*" %%A in ('dir /s "dist\LINK.exe"') do echo %%A
  echo.
  echo Ready for distribution!
) else (
  echo.
  echo ✗ Build failed - LINK.exe not found
  echo.
)

pause
