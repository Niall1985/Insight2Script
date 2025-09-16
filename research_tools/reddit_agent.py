import praw
import os
from dotenv import load_dotenv
load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv('client_id'),
    client_secret=os.getenv('client_secret'),
    user_agent=os.getenv('user_agent')
)

def fetch_reddit_text_posts(topic, limit=20):
    posts = []
    
    for submission in reddit.subreddit('all').search(topic, limit=limit, time_filter='month'):
        if submission.selftext and len(submission.selftext.strip()) > 0:
            posts.append({
                'title': submission.title,
                'selftext': submission.selftext,
                'subreddit': submission.subreddit.display_name,
                'url': submission.url,
                'score': submission.score,
                'created_utc': submission.created_utc
            })
    
    return posts

if __name__ == "__main__":
    topic = "Nikola Tesla"
    text_posts = fetch_reddit_text_posts(topic, limit=10)
    
    for idx, post in enumerate(text_posts):
        print(f"{idx+1}. Title: {post['title']}")
        print(f"   Text: {post['selftext'][:300]}...")
        print(f"   URL: {post['url']}\n")
