# config.py

import os
from dotenv import load_dotenv

load_dotenv()

# ===================
# API KEYS
# ===================

# Get from: https://console.groq.com/keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Get from: Make.com webhook trigger
WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL", "").strip('"')

# ===================
# RSS FEEDS (AI NEWS)
# ===================

RSS_FEEDS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "https://feeds.feedburner.com/venturebeat/SZYF",
    "https://www.technologyreview.com/feed/",
    "https://blog.google/technology/ai/rss/",
]

# ===================
# SETTINGS
# ===================

YOUR_NAME = "Your Name"
YOUR_STYLE = "professional but friendly, add emojis, include engaging CTAs"
MAX_NEWS_ITEMS = 5

