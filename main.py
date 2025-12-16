# main.py

import schedule
import time
from datetime import datetime

# Import your helper modules
from news_fetcher import get_top_news
from post_generator import generate_linkedin_post
# We changed BufferPoster to WebhookPoster here:
from linkedin_poster import WebhookPoster, LocalSaver

def run_automation(post_online=False):
    """
    Main automation function
    """
    print("\n" + "="*60)
    print(f"🚀 LinkedIn AI Automation Started")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Step 1: Fetch latest news
    print("\n📰 STEP 1: Fetching latest AI news...")
    news_items = get_top_news(count=1)  # Get top 1 news
    
    if not news_items:
        print("❌ No news found. Exiting.")
        return
    
    news = news_items[0]
    print(f"✅ Selected: {news['title'][:60]}...")
    
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
    
    # Fetch and generate
    news_items = get_top_news(count=1)
    if not news_items:
        print("❌ No news found.")
        return
    
    news = news_items[0]
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