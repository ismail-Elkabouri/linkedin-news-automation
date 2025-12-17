# main.py

import schedule
import time
from datetime import datetime

# Import your helper modules
from news_fetcher import get_top_news
from post_generator import generate_linkedin_post
# We changed BufferPoster to WebhookPoster here:
from linkedin_poster import WebhookPoster, LocalSaver

def select_news_article(news_items):
    """
    Display news articles with ranking scores and let user choose one
    """
    if not news_items:
        print("❌ No news found. Exiting.")
        return None
    
    print("\n📰 Found LLM News Articles (Ranked by Quality):")
    print("="*80)
    
    for i, news in enumerate(news_items, 1):
        score = news.get('rank_score', 0)
        # Create a visual score bar
        score_bar = "█" * (score // 5) + "░" * ((100 - score) // 5)
        print(f"\n{i}. [{score_bar}] Score: {score}/100")
        print(f"   Title: {news['title'][:70]}")
        print(f"   Source: {news['source']}")
        print(f"   Summary: {news['summary'][:100]}...")
    
    print("\n" + "="*80)
    choice = input(f"\nChoose article (1-{len(news_items)}) or 0 to exit: ").strip()
    
    try:
        choice_num = int(choice)
        if choice_num == 0:
            print("⏭ Skipped.")
            return None
        elif 1 <= choice_num <= len(news_items):
            selected = news_items[choice_num - 1]
            print(f"✅ Selected article with score {selected.get('rank_score', 0)}/100")
            return selected
        else:
            print(f"❌ Invalid choice. Please enter 1-{len(news_items)}")
            return select_news_article(news_items)  # Ask again
    except ValueError:
        print("❌ Invalid input. Please enter a number.")
        return select_news_article(news_items)  # Ask again


def run_automation(post_online=False):
    """
    Main automation function
    """
    print("\n" + "="*60)
    print(f"🚀 LinkedIn AI Automation Started")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Step 1: Fetch latest news
    print("\n📰 STEP 1: Fetching latest LLM news...")
    news_items = get_top_news(count=5)  # Get top 5 news
    
    if not news_items:
        print("❌ No news found. Exiting.")
        return
    
    # Step 1b: Let user choose which article
    print("\n🔍 STEP 1b: Choose an article to post")
    news = select_news_article(news_items)
    
    if not news:
        return
    
    print(f"\n✅ Selected: {news['title'][:60]}...")
    
    # Step 2: Generate LinkedIn post
    print("\n🤖 STEP 2: Generating LinkedIn post with AI...")
    post_content = generate_linkedin_post(news)
    
    if not post_content:
        print("❌ Failed to generate post. Exiting.")
        return
    
    print("\n📝 Generated Post:")
    print("-"*40)
    print(post_content)
    print("-"*40)
    
    # Step 3: Post or Save
    print("\n📤 STEP 3: Publishing post...")
    
    if post_online:
        # Use the WebhookPoster to send to Make.com
        poster = WebhookPoster()
        poster.post_to_webhook(post_content, news['title'])
    else:
        # Save locally for manual posting
        saver = LocalSaver()
        saver.save_post(post_content, news['title'])
    
    print("\n✅ AUTOMATION COMPLETE!")
    print("="*60)


def run_with_approval():
    """
    Generate post but ask for approval before posting
    """
    print("\n" + "="*60)
    print(f"🚀 LinkedIn AI Automation (With Approval)")
    print("="*60)
    
    # Fetch and let user choose
    print("\n📰 Fetching latest LLM news...")
    news_items = get_top_news(count=5)
    if not news_items:
        print("❌ No news found.")
        return
    
    print("\n🔍 Choose an article to post")
    news = select_news_article(news_items)
    
    if not news:
        return
    
    post_content = generate_linkedin_post(news)
    
    if not post_content:
        print("❌ Failed to generate post.")
        return
    
    # Show post
    print("\n📝 Generated Post:")
    print("-"*40)
    print(post_content)
    print("-"*40)
    
    # Ask for approval
    print("\n🤔 What would you like to do?")
    print("1. Save to file (for manual posting)")
    print("2. Post to LinkedIn (via Make.com)")
    print("3. Regenerate")
    print("4. Skip")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        saver = LocalSaver()
        saver.save_post(post_content, news['title'])
    elif choice == "2":
        poster = WebhookPoster()
        poster.post_to_webhook(post_content, news['title'])
    elif choice == "3":
        run_with_approval()  # Recursively regenerate
    else:
        print("⏭ Skipped.")


def run_scheduled(hour=9, minute=0):
    """
    Run automation on a schedule
    """
    schedule_time = f"{hour:02d}:{minute:02d}"
    
    print(f"⏰ Scheduled to run daily at {schedule_time}")
    print("Press Ctrl+C to stop\n")
    
    # Use post_online=True for scheduled runs
    schedule.every().day.at(schedule_time).do(run_automation, post_online=True)
    
    while True:
        schedule.run_pending()
        time.sleep(60)


# ===================
# RUN THE SCRIPT
# ===================

if __name__ == "__main__":
    print("\n🤖 LINKEDIN AI AUTOMATION")
    print("="*40)
    print("1. Run once (save to file)")
    print("2. Run once (with approval)")
    print("3. Run once (post to LinkedIn immediately)")
    print("4. Run on schedule (daily)")
    print("="*40)
    
    choice = input("Choose option (1-4): ").strip()
    
    if choice == "1":
        run_automation(post_online=False)
    elif choice == "2":
        run_with_approval()
    elif choice == "3":
        run_automation(post_online=True)
    elif choice == "4":
        hour = int(input("Post at hour (0-23): ") or "9")
        run_scheduled(hour=hour)
    else:
        print("Invalid choice")