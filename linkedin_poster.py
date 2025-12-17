# linkedin_poster.py

import requests
import json
import os
from config import WEBHOOK_URL


class WebhookPoster:
    """
    Post to LinkedIn via webhook (e.g., Make.com)
    """
    
    def __init__(self, webhook_url=None):
        self.webhook_url = webhook_url or WEBHOOK_URL
    
    def post_to_webhook(self, content, post_title=""):
        """
        Send post to webhook endpoint
        """
        if not self.webhook_url:
            print("❌ No webhook URL configured. Set WEBHOOK_URL in .env file.")
            return False
        
        payload = {
            "title": post_title,
            "text": content,
            "content": content,
            "timestamp": self._get_timestamp()
        }
        
        try:
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            
            if response.status_code in [200, 201, 202]:
                print("✅ Post sent to webhook successfully!")
                return True
            else:
                print(f"❌ Webhook error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error posting to webhook: {e}")
            return False
    
    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class BufferPoster:
    """
    Post to LinkedIn via Buffer API (free tier)
    """
    
    def __init__(self):
        self.access_token = BUFFER_ACCESS_TOKEN
        self.base_url = "https://api.bufferapp.com/1"
        self.profile_id = None
    
    
    def get_profiles(self):
        """
        Get your Buffer profiles (LinkedIn, etc.)
        """
        url = f"{self.base_url}/profiles.json"
        params = {"access_token": self.access_token}
        
        try:
            response = requests.get(url, params=params)
            profiles = response.json()
            
            print("\n📱 Your Buffer Profiles:")
            for profile in profiles:
                print(f"   - {profile['service']}: {profile['id']}")
                
                # Auto-select LinkedIn profile
                if profile['service'] == 'linkedin':
                    self.profile_id = profile['id']
            
            return profiles
            
        except Exception as e:
            print(f"❌ Error getting profiles: {e}")
            return []
    
    
    def post_to_buffer(self, content, profile_id=None):
        """
        Add post to Buffer queue
        """
        if profile_id is None:
            profile_id = self.profile_id
            
        if profile_id is None:
            print("❌ No LinkedIn profile found. Run get_profiles() first.")
            return False
        
        url = f"{self.base_url}/updates/create.json"
        
        data = {
            "access_token": self.access_token,
            "profile_ids[]": [profile_id],
            "text": content,
        }
        
        try:
            response = requests.post(url, data=data)
            result = response.json()
            
            if result.get("success"):
                print("✅ Post added to Buffer queue!")
                return True
            else:
                print(f"❌ Buffer error: {result}")
                return False
                
        except Exception as e:
            print(f"❌ Error posting to Buffer: {e}")
            return False


class LocalSaver:
    """
    Alternative: Save posts locally for manual posting
    (Use this if you don't want Buffer)
    """
    
    def __init__(self, filename="generated_posts.txt"):
        self.filename = filename
    
    
    def save_post(self, post_content, news_title):
        """
        Save post to local file
        """
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write("\n" + "="*60 + "\n")
            f.write(f"📰 Based on: {news_title}\n")
            f.write(f"📅 Generated: {self._get_timestamp()}\n")
            f.write("-"*60 + "\n\n")
            f.write(post_content)
            f.write("\n\n")
        
        print(f"💾 Post saved to {self.filename}")
        return True
    
    
    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Test
if __name__ == "__main__":
    # Test local saver
    saver = LocalSaver()
    saver.save_post("This is a test post!", "Test News Title")
    
    # Test Buffer (uncomment if you have token)
    # buffer = BufferPoster()
    # buffer.get_profiles()
