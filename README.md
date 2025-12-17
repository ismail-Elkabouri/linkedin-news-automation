# LinkedIn AI News Automation 🚀

Automatically fetch AI/ML news from multiple sources and post professionally formatted content to LinkedIn using AI-generated posts. Perfect for maintaining an active LinkedIn presence without manual effort!

**Now Available as a Desktop App!** 🎉 Download `LINK.exe` - no installation needed!

## Features ✨

- 📰 **Multi-source News Fetching**: Aggregates AI/ML news from 5 RSS feeds (TechCrench, The Verge, VentureBeat, MIT Technology Review, Google AI Blog)
- 🤖 **AI-Powered Content Generation**: Uses Groq's LLaMA model to generate professional, engaging LinkedIn posts
- 📱 **Smart Formatting**: Automatically adds emojis, bold hooks, and compelling CTAs
- 🔗 **LinkedIn Integration**: Posts directly to LinkedIn via Make.com webhooks
- 💻 **Desktop GUI App**: Beautiful terminal-style interface (PyQt5)
- ✏️ **Editable Posts**: Edit generated content before posting
- 🎯 **3 Posting Modes**:
  - **Mode 1**: Save posts to file for manual review
  - **Mode 2**: Generate with approval before posting
  - **Mode 3**: Auto-post immediately
- ⏰ **Scheduling Support**: Run daily at a specific time
- 🎨 **Professional Posts**: Posts include formatted text, emojis, and link previews
- 🔒 **Secure**: Masked API keys and webhook URLs

## Quick Start (Desktop App) 🚀

### For Users:
1. **Download** `LINK.exe` from [Releases](https://github.com/ismail-Elkabouri/linkedin-news-automation/releases)
2. **Run** LINK.exe (no Python installation needed!)
3. **Configure** in Settings [3]:
   - Add your Groq API Key (get from https://console.groq.com)
   - Add your Make.com Webhook URL
4. **Start using**:
   - Press `F` to fetch news
   - Press `G` to generate posts
   - Edit posts directly in the app
   - Post or save to file

**Keyboard Shortcuts:**
| Key | Action |
|-----|--------|
| F | Fetch news |
| G | Generate post |
| 1 | News Feed |
| 2 | Post Generator |
| 3 | Settings |
| 4 | About |

## Architecture 🏗️

```
linkedin-automation/
├── gui_app.py             # PyQt5 Desktop GUI application
├── build_exe.py           # Script to build LINK.exe
├── config.py              # Configuration management
├── news_fetcher.py        # RSS feed aggregation & ranking
├── post_generator.py      # AI post generation with Groq
├── linkedin_poster.py     # LinkedIn posting via Make.com webhook
├── main.py                # CLI and automation orchestration
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── README_DISTRIBUTION.md # Distribution guide
└── .gitignore            # Git ignore rules
```

## Prerequisites 📋

### For Desktop App:
- **Windows 7 or later**
- **Groq API Key** (free at https://console.groq.com)
- **Make.com Account** (free tier available)
- **Internet connection**

### For CLI:
- **Python 3.8+**
- **Groq API Key** (free at https://console.groq.com)
- **Make.com Account** (free tier available)

## Installation 🔧

### Desktop App (Recommended - Easiest)
1. Download `LINK.exe` from [Releases](https://github.com/ismail-Elkabouri/linkedin-news-automation/releases)
2. Run the executable
3. Go to Settings [3] and configure:
   - GROQ_API_KEY
   - MAKE_WEBHOOK_URL
4. Click SAVE SETTINGS

### CLI (Command Line)

#### 1. Clone the repository
```bash
git clone https://github.com/ismail-Elkabouri/linkedin-news-automation.git
cd linkedin-news-automation
```

#### 2. Install dependencies
```bash
pip install -r requirements.txt
```

#### 3. Set up environment variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
GROQ_API_KEY=your_groq_api_key_here
MAKE_WEBHOOK_URL=your_make_webhook_url_here
```

**Getting your credentials:**
- **GROQ_API_KEY**: Get it from https://console.groq.com
- **MAKE_WEBHOOK_URL**: Create a scenario in Make.com with a webhook trigger and copy the URL

#### 4. Build your own .exe (Optional)
```bash
pip install pyinstaller
python build_exe.py
```

## GUI Features 🎨

### News Feed Page
- Real-time fetching from 5 RSS sources
- Automatic LLM article filtering
- Quality ranking (0-100 score)
- Click to select articles

### Post Generator Page
- AI-powered content generation using Groq API
- **Fully editable post text** before posting
- Character counter
- Save, Post, or Copy options

### Settings Page
- Configure Groq API Key (secure - masked input)
- Configure Make.com Webhook URL (secure - masked input)
- Display options (scanline, glow effects)
- Save settings to .env file

### About Page
- App information
- Keyboard shortcuts reference
- Version history

### Option 1: Save to File (Review Later)
```bash
python main.py
# Then select: 1
```
Posts are saved to `generated_posts.txt` for manual review.

### Option 2: Review & Approve Before Posting
```bash
python main.py
# Then select: 2
```
Shows the generated post and asks for your approval:
- **1**: Save to file
- **2**: Post to LinkedIn
- **3**: Regenerate (different post for same article)
- **4**: Skip

### Option 3: Post Immediately (Fastest)
```bash
python main.py
# Then select: 3
```
Automatically fetches, generates, and posts without any prompts.

### Option 4: Schedule Daily Posts
```bash
python main.py
# Then select: 4
# Enter hour (0-23, e.g., 9 for 9 AM)
```
**Note**: Your PC must be running at the scheduled time, or use Windows Task Scheduler for background execution.

## How It Works 🔄

### Desktop App Flow:
```
1. Run LINK.exe
   ↓
2. Go to Settings, configure API keys
   ↓
3. Go to News Feed, click FETCH NEWS
   ↓
4. Browse articles (ranked by quality)
   ↓
5. Click article to select
   ↓
6. Go to Generator, click GENERATE POST
   ↓
7. Edit post text as needed
   ↓
8. Click SAVE or POST TO LINK
   ↓
9. If posting: Sends to Make.com webhook
   ↓
10. Make.com → Buffer → LinkedIn
```

### CLI Flow:

```
1. User runs main.py
   ↓
2. Fetches latest AI news from RSS feeds
   ↓
3. Selects the most relevant article (auto or manual)
   ↓
4. Generates professional post using Groq AI
   ↓
5. User chooses action (save/review/post/schedule)
   ↓
6. If posting: Sends to Make.com webhook
   ↓
7. Make.com → Buffer → LinkedIn
```

## Post Format Example 📝

```
🍴📱💻 **DoorDash Unveils AI-Powered Social App**

DoorDash is revolutionizing the way we discover new restaurants with the launch 
of Zesty, an AI-driven social app. Users can share photos and comments about their 
dining experiences, discover new content from others, and follow fellow food 
enthusiasts just like on social media. 💬
...more

https://techcrunch.com/2025/12/16/doordash-rolls-out-zesty-an-ai-social-app-for-discovering-new-restaurants/
```

## Configuration 📋

### RSS Feed Sources
Edit `config.py` to change news sources:
```python
RSS_FEEDS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://www.theverge.com/rss/ai-artificial-intelligence",
    "https://feeds.feedburner.com/venturebeat/SZYF",
    "https://www.technologyreview.com/feed/",
    "https://blog.google/technology/ai/rss/"
]
```

### Post Generation
Edit `post_generator.py` to customize:
- Post tone and style
- Emoji usage
- Word count limits
- CTA (Call-To-Action) style

## Requirements 📦

```
requests==2.31.0          # HTTP requests
python-dotenv==1.0.0      # Environment variables
feedparser==6.0.10        # RSS feed parsing
groq==0.5.0              # Groq AI API
schedule==1.2.0          # Task scheduling
```

## Workflow Diagram 🔀

```
┌─────────────────┐
│  Start Script   │
└────────┬────────┘
         ↓
┌─────────────────────────────┐
│ Load config from .env       │
└────────┬────────────────────┘
         ↓
┌─────────────────────────────┐
│ Fetch news from RSS feeds   │
└────────┬────────────────────┘
         ↓
┌─────────────────────────────┐
│ Select top article          │
└────────┬────────────────────┘
         ↓
┌─────────────────────────────┐
│ Generate post with Groq AI  │
└────────┬────────────────────┘
         ↓
    ┌────┴─────┬─────────┬──────────┐
    ↓          ↓         ↓          ↓
 [Save]    [Approve]  [Auto]  [Schedule]
    │          │        │          │
    └──────────┴────────┴──────────┘
              ↓
     ┌────────────────────┐
     │ Post to LinkedIn   │
     │ via Make.com       │
     └────────────────────┘
```

## Troubleshooting 🔧

### "No webhook URL configured"
- Make sure `.env` file exists with `MAKE_WEBHOOK_URL` set
- Verify the URL is correct from your Make.com scenario

### "Failed to generate post"
- Check your `GROQ_API_KEY` is valid
- Ensure you have API quota remaining
- Check internet connection

### "No news found"
- RSS feeds might be temporarily unavailable
- Check your internet connection
- Wait a moment and try again

## Advanced Usage 🚀

### Windows Task Scheduler (For 24/7 Automation)
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger to daily at 9 AM
4. Set action to run: `python main.py`
5. Set working directory to project folder

### Cloud Deployment
Deploy to a VPS or cloud server for 24/7 automated posting:
- AWS EC2
- DigitalOcean
- Heroku
- Google Cloud

## Contributing 🤝

Feel free to:
- Report bugs
- Suggest improvements
- Add new RSS feed sources
- Improve post generation
- Add new features

## License 📄

MIT License - Feel free to use this project for personal or commercial purposes.

## Support 💬

For issues or questions:
1. Check the Troubleshooting section
2. Review your `.env` configuration
3. Check Make.com scenario settings
4. Open an issue on GitHub

## Disclaimer ⚠️

- Ensure you have rights to share content from the sources
- Respect LinkedIn's Terms of Service
- Don't spam or post excessively
- Use responsibly!

---

**Made with ❤️ for LinkedIn automation enthusiasts**

Happy posting! 🚀📱
