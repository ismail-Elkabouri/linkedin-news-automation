# LINK - AI News Automation App

**Standalone Desktop Application for Automated LinkedIn Post Generation**

## Quick Start

### For Users (Using the .exe)

1. **Download** `LINK.exe` from the releases
2. **Run** `LINK.exe` - no installation needed!
3. **Configure** in Settings [3]:
   - Add your Groq API Key
   - Add your Make.com Webhook URL
   - Click SAVE SETTINGS
4. **Start Using**:
   - Fetch news with [F] or click "FETCH NEWS"
   - Generate posts with [G] or click "GENERATE POST"
   - Edit posts in the text box
   - Post to LinkedIn or save locally

### Requirements
- Windows 7 or later
- Internet connection
- Groq API key (free from https://console.groq.com)
- Make.com webhook URL

---

## For Developers (Building from Source)

### Build the .exe

```bash
# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Build executable
python build_exe.py

# Or use PyInstaller directly
pyinstaller --onefile --windowed --name=LINK gui_app.py
```

### Output
- `LINK.exe` - Standalone executable (in `dist/` and project root)
- Can be distributed without Python installed
- Self-contained with all dependencies

### Setup for Distribution

1. Update `requirements.txt` with pinned versions:
```bash
pip freeze > requirements.txt
```

2. Create `.env.example` template:
```
GROQ_API_KEY=your_groq_api_key_here
MAKE_WEBHOOK_URL=https://hook.eu1.make.com/...
```

3. Push to GitHub with:
   - `LINK.exe` (in releases or artifacts)
   - `README.md` with user instructions
   - `.env.example` (not actual `.env`)
   - `build_exe.py` for developers
   - `requirements.txt`

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `F` | Fetch news |
| `G` | Generate post |
| `1` | News Feed |
| `2` | Post Generator |
| `3` | Settings |
| `4` | About |

---

## Architecture

```
┌─────────────────────┐
│   LINK.exe (GUI)    │
│   (gui_app.py)      │
└──────────┬──────────┘
           │
    ┌──────┴──────┐
    │             │
┌───▼────┐  ┌────▼────┐
│ News   │  │ Post     │
│Fetcher │  │Generator │
└────────┘  └─────┬────┘
                  │
            ┌─────▼──────┐
            │  Groq API  │
            │  (LLaMA)   │
            └──────┬─────┘
                   │
            ┌──────▼──────┐
            │  Webhook    │
            │ (Make.com)  │
            └──────┬──────┘
                   │
            ┌──────▼──────┐
            │  LinkedIn   │
            │  (via Buffer)
            └─────────────┘
```

---

## Troubleshooting

### "Failed to post" error
- Check webhook URL in Settings [3]
- Verify Make.com scenario is active
- Ensure Groq API key is valid

### News not fetching
- Check internet connection
- Verify RSS feeds are accessible
- Check Groq API key has usage quota

### .env not loading
- Ensure `.env` file exists in same directory as `LINK.exe`
- Use Settings [3] to configure instead

---

## Version History

### v1.0.0 (2024.01.15)
- Initial release
- Terminal-style UI
- Real-time news fetching
- AI post generation with Groq
- Settings management
- Post editing & publishing
- Security: Masked API keys & webhooks

---

## License

MIT License - See LICENSE file

---

## Support

For issues or feature requests:
1. Check `.env` configuration
2. Verify API keys are valid
3. Check Make.com webhook status
4. Review logs in the terminal window

---

**Made with ❤️ for AI/LLM enthusiasts**
