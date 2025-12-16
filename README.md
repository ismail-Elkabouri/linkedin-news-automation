# LinkedIn AI News Automation 🚀

Automatically fetch AI/ML news from multiple sources and post professionally formatted content to LinkedIn using AI-generated posts. Perfect for maintaining an active LinkedIn presence without manual effort!

## Features ✨

- 📰 **Multi-source News Fetching**: Aggregates AI/ML news from 5 RSS feeds (TechCrunch, The Verge, VentureBeat, MIT Technology Review, Google AI Blog)
- 🤖 **AI-Powered Content Generation**: Uses Groq's LLaMA model to generate professional, engaging LinkedIn posts
- 📱 **Smart Formatting**: Automatically adds emojis, bold hooks, and compelling CTAs
- 🔗 **LinkedIn Integration**: Posts directly to LinkedIn via Make.com webhooks
- 🎯 **3 Posting Modes**:
  - **Mode 1**: Save posts to file for manual review
  - **Mode 2**: Generate with approval before posting
  - **Mode 3**: Auto-post immediately
- ⏰ **Scheduling Support**: Run daily at a specific time
- 🎨 **Professional Posts**: Posts include formatted text, emojis, and link previews

## Architecture 🏗️

```
linkedin-automation/
├── config.py              # Configuration management
├── news_fetcher.py        # RSS feed aggregation
├── post_generator.py      # AI post generation with Groq
├── linkedin_poster.py     # LinkedIn posting via Make.com webhook
├── main.py                # CLI and automation orchestration
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (credentials)
└── .gitignore            # Git ignore rules
```

## Prerequisites 📋

- **Python 3.8+**
- **Groq API Key** (free at https://console.groq.com)
- **Make.com Account** (free tier available)
- **Buffer Account** (optional, for scheduling)

## Installation 🔧

### 1. Clone the repository
```bash
git clone https://github.com/ismail-Elkabouri/linkedin-news-automation.git
cd linkedin-news-automation
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
MAKE_WEBHOOK_URL=your_make_webhook_url_here
```

**Getting your credentials:**
- **GROQ_API_KEY**: Get it from https://console.groq.com
- **MAKE_WEBHOOK_URL**: Create a scenario in Make.com with a webhook trigger and copy the URL

## Usage 🎯

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

```
1. User runs the script
   ↓
2. Fetches latest AI news from RSS feeds
   ↓
3. Selects the most relevant article
   ↓
4. Generates professional post using Groq AI
   ↓
5. User chooses action (save/review/post immediately)
   ↓
6. If posting: Sends to Make.com webhook
   ↓
7. Make.com triggers Buffer
   ↓
8. Buffer posts to LinkedIn
   ↓
9. Post appears on your LinkedIn profile!
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
