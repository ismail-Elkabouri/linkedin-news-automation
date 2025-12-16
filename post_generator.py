# post_generator.py

from groq import Groq
from config import GROQ_API_KEY, YOUR_NAME, YOUR_STYLE


# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


def generate_linkedin_post(news_item):
    """
    Use AI to generate a LinkedIn post from news
    """
    
    prompt = f"""
You are a LinkedIn content creator specializing in AI and technology news.

Create a SHORT, professional LinkedIn post based on this news. Make it visually appealing with emojis.

TITLE: {news_item['title']}
SUMMARY: {news_item['summary']}
SOURCE: {news_item['source']}

REQUIREMENTS:
- Start with 2-3 relevant emojis that represent the topic
- Add emoji + Bold Hook (max 10 words)
- Main text: 2-3 sentences ONLY (50-80 words)
- Add "...more" to encourage clicks
- NO hashtags in the post body
- Clean, professional, easy to scan
- End with ONE engaging question
- Use relevant emojis throughout to break up text (2-3 total)

Example format:
🚀💡 **Your Bold Hook Here**
Short summary. 🤖 Second sentence with emoji. ...more

What are your thoughts?

Write the post now:
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Free and fast
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert LinkedIn content creator focusing on AI/ML topics."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=250
        )
        
        post_content = response.choices[0].message.content
        
        # Format: Put link at END to trigger preview generation
        # LinkedIn works better when link is after the text
        full_post = f"{post_content}\n\n{news_item['link']}"
        
        return full_post
        
    except Exception as e:
        print(f"❌ Error generating post: {e}")
        return None


def generate_multiple_posts(news_items):
    """
    Generate posts for multiple news items
    """
    posts = []
    
    for item in news_items:
        print(f"\n🤖 Generating post for: {item['title'][:50]}...")
        post = generate_linkedin_post(item)
        
        if post:
            posts.append({
                "news": item,
                "post": post
            })
            print("✅ Post generated!")
    
    return posts


# Test
if __name__ == "__main__":
    test_news = {
        "title": "OpenAI releases GPT-5",
        "summary": "OpenAI has announced GPT-5 with improved reasoning.",
        "link": "https://example.com",
        "source": "TechCrunch"
    }
    
    post = generate_linkedin_post(test_news)
    print("\n" + "="*50)
    print(post)