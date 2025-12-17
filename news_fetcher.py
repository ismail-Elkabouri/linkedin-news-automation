# news_fetcher.py

import feedparser
from datetime import datetime, timedelta
from config import RSS_FEEDS, MAX_NEWS_ITEMS, LLM_KEYWORDS, FILTER_LLM_ONLY


def is_llm_related(title, summary):
    """
    Check if news is related to LLMs using keyword filtering
    """
    if not FILTER_LLM_ONLY:
        return True
    
    text = (title + " " + summary).lower()
    return any(keyword in text for keyword in LLM_KEYWORDS)


def rank_news_article(news_item):
    """
    Rank a news article based on relevance and quality signals
    Returns a score between 0-100
    """
    score = 0
    title = news_item['title'].lower()
    summary = news_item['summary'].lower()
    text = title + " " + summary
    
    # High-value LLM keywords (stronger signals)
    premium_keywords = {
        "gpt": 10,
        "claude": 10,
        "gemini": 8,
        "llama": 8,
        "deepseek": 8,
        "reasoning": 12,
        "breakthrough": 15,
        "release": 8,
        "announcement": 7,
        "new model": 12,
        "fine-tune": 6,
        "state-of-the-art": 12,
        "sota": 10,
        "performance": 5,
        "training": 6,
        "inference": 5,
    }
    
    # Count premium keyword matches
    for keyword, points in premium_keywords.items():
        if keyword in text:
            score += points
    
    # Bonus for title matches (title is more important than summary)
    for keyword in premium_keywords.keys():
        if keyword in title:
            score += 3
    
    # Penalty for older articles (freshness bonus for recent ones)
    try:
        if news_item['published']:
            pub_date = datetime.fromisoformat(news_item['published'].replace('Z', '+00:00'))
            days_old = (datetime.now(pub_date.tzinfo) - pub_date).days
            if days_old <= 1:
                score += 20  # Very recent
            elif days_old <= 3:
                score += 10  # Recent
            elif days_old <= 7:
                score += 5   # This week
    except:
        pass  # If date parsing fails, no bonus/penalty
    
    # Length bonus (longer, more detailed articles tend to be better)
    if len(news_item['summary']) > 300:
        score += 5
    
    # Cap score at 100
    return min(score, 100)


def rank_and_sort_news(news_items):
    """
    Rank all news items and sort by score
    Returns list of news with scores attached
    """
    ranked_news = []
    for news in news_items:
        score = rank_news_article(news)
        news['rank_score'] = score
        ranked_news.append(news)
    
    # Sort by score descending
    ranked_news.sort(key=lambda x: x['rank_score'], reverse=True)
    return ranked_news


def fetch_latest_news():
    """
    Fetch latest LLM news from RSS feeds
    Returns list of news items filtered for LLM content
    """
    all_news = []
    
    for feed_url in RSS_FEEDS:
        try:
            print(f"📡 Fetching: {feed_url[:50]}...")
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries[:MAX_NEWS_ITEMS * 3]:  # Fetch more to account for filtering
                title = entry.get("title", "")
                summary = entry.get("summary", "")[:500]
                
                # Filter for LLM-related content
                if is_llm_related(title, summary):
                    news_item = {
                        "title": title,
                        "summary": summary,
                        "link": entry.get("link", ""),
                        "source": feed.feed.get("title", "Unknown"),
                        "published": entry.get("published", "")
                    }
                    all_news.append(news_item)
                    
                    if len(all_news) >= MAX_NEWS_ITEMS * 2:
                        break  # Stop fetching from this feed if we have enough
                
        except Exception as e:
            print(f"❌ Error fetching {feed_url}: {e}")
            continue
    
    print(f"✅ Found {len(all_news)} news items")
    return all_news


def get_top_news(count=1):
    """
    Get the best ranked news items
    """
    news = fetch_latest_news()
    
    # Rank and sort by quality score
    ranked_news = rank_and_sort_news(news)
    
    return ranked_news[:count]


# Test
if __name__ == "__main__":
    news = get_top_news(3)
    for item in news:
        print(f"\n📰 {item['title']}")
        print(f"   Source: {item['source']}")