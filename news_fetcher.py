# news_fetcher.py

import feedparser
from datetime import datetime, timedelta
from config import RSS_FEEDS, MAX_NEWS_ITEMS


def fetch_latest_news():
    """
    Fetch latest AI/ML news from RSS feeds
    Returns list of news items
    """
    all_news = []
    
    for feed_url in RSS_FEEDS:
        try:
            print(f"📡 Fetching: {feed_url[:50]}...")
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries[:MAX_NEWS_ITEMS]:
                news_item = {
                    "title": entry.get("title", ""),
                    "summary": entry.get("summary", "")[:500],
                    "link": entry.get("link", ""),
                    "source": feed.feed.get("title", "Unknown"),
                    "published": entry.get("published", "")
                }
                all_news.append(news_item)
                
        except Exception as e:
            print(f"❌ Error fetching {feed_url}: {e}")
            continue
    
    print(f"✅ Found {len(all_news)} news items")
    return all_news


def get_top_news(count=1):
    """
    Get the most relevant news items
    """
    news = fetch_latest_news()
    
    # Sort by most recent (simple approach)
    # You could add more sophisticated ranking
    return news[:count]


# Test
if __name__ == "__main__":
    news = get_top_news(3)
    for item in news:
        print(f"\n📰 {item['title']}")
        print(f"   Source: {item['source']}")