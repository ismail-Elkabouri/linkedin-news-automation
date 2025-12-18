# LINK App - Release Instructions

## For Users (Downloading LINK.exe)

1. **Download** `LINK.exe` from the [Latest Release](https://github.com/ismail-Elkabouri/linkedin-news-automation/releases)
2. **Run** LINK.exe (no installation needed!)
3. **Configure** in Settings [3]:
   - Add your Groq API Key (get from https://console.groq.com)
   - Add your Make.com Webhook URL
4. **Start using**:
   - Press `F` to fetch news
   - Press `G` to generate posts
   - Edit posts directly in the app
   - Post or save to file

## For Developers (Building LINK.exe)

### Prerequisites
- Python 3.8+
- Windows OS (for .exe build)

### Build Steps

```bash
# 1. Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# 2. Build executable
pyinstaller --onefile --windowed --name=LINK gui_app.py

# 3. Find the executable
# Output: dist/LINK.exe (~200-300 MB)
```

### Alternative Method (Using Batch File)

```cmd
# Run the build script
build_link.bat
```

### Build Troubleshooting

If you encounter issues:
1. **Clean previous builds:**
   ```cmd
   rmdir /s /q dist build
   del LINK.spec
   ```

2. **Install missing dependencies:**
   ```bash
   pip install PyQt5==5.15.9
   pip install pyinstaller
   ```

3. **Try with hidden imports:**
   ```bash
   pyinstaller --onefile --windowed --name=LINK \
     --hidden-import=PyQt5 \
     --hidden-import=PyQt5.QtWidgets \
     --hidden-import=PyQt5.QtCore \
     --hidden-import=PyQt5.QtGui \
     gui_app.py
   ```

## File Sizes
- `LINK.exe`: ~200-300 MB (includes all dependencies)
- `gui_app.py`: ~150 KB (source code only)

## Distribution Notes
- No Python installation required for users
- All dependencies bundled in single .exe
- Runs on Windows 7+
- Configuration stored in `.env` file in same directory

## Security
- API keys and webhook URLs are masked in UI
- Configuration file should be kept private
- Never share `.env` file publicly
