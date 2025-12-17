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
# RSS FEEDS (LLM NEWS ONLY)
# ===================

RSS_FEEDS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "https://feeds.feedburner.com/venturebeat/SZYF",
    "https://www.technologyreview.com/feed/",
    "https://blog.google/technology/ai/rss/",
]

# ===================
# LLM FILTERING
# ===================

# Keywords to filter for LLM-related news only
LLM_KEYWORDS = [
    "llm", "large language model", "gpt", "chatgpt", "claude", "gemini",
    "mistral", "llama", "deepseek", "qwen", "grok", "groq",
    "language model", "transformer", "fine-tune", "prompt engineering",
    "token", "inference", "reasoning model"
]

# Enable/disable LLM filtering
FILTER_LLM_ONLY = True

# ===================
# SETTINGS
# ===================

YOUR_NAME = "Your Name"
YOUR_STYLE = "professional but friendly, add emojis, include engaging CTAs"
MAX_NEWS_ITEMS = 5

