import praw
import os
import json
from dotenv import load_dotenv
from pathlib import Path

# Get the backend directory
backend_dir = Path(__file__).resolve().parents[2]
load_dotenv(backend_dir / ".env")

reddit = praw.Reddit(
    client_id=os.environ['CLIENT_ID'],
    client_secret=os.environ['CLIENT_SECRET'],
    user_agent=os.environ['USER_AGENT']
)

def process_comment(comment):
    return {
        "id": comment.id,
        "body": comment.body,
        "created_UTC": comment.created_utc,
        "replies": [process_comment(reply) for reply in comment.replies if isinstance(reply, praw.models.Comment)],
        "score": comment.score,
        "parent_id": comment.parent_id[3:],
        "link_id": comment.link_id
    }

def get_thelastofus_posts():
    subreddit = reddit.subreddit("thelastofus")
    query = 'review' # Look for posts that include the word 'review'
    
    # Create data directories if they don't exist
    data_dir = backend_dir / "data"
    raw_dir = data_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    # Load existing data if file exists
    json_file = raw_dir / "reddit_data.json"
    existing_posts = []
    if json_file.exists():
        try:
            with open(json_file, 'r') as f:
                existing_posts = json.load(f)
                if not isinstance(existing_posts, list):
                    existing_posts = [existing_posts]  # Convert single post to list
        except json.JSONDecodeError:
            print("Error reading JSON file, starting with empty list")
            existing_posts = []
    
    # Get existing post IDs
    existing_ids = {post.get('id') for post in existing_posts if isinstance(post, dict)}
    
    for submission in subreddit.search(query, sort='relevance', time_filter='all', limit=30):  # change the limit as needed
        # Skip if post already exists
        if submission.id in existing_ids:
            print(f"Post with ID {submission.id} already exists. Skipping...")
            continue
            
        reddit_post = {
            "id": submission.id,
            "title": submission.title,
            "created_UTC": submission.created_utc,
            "url": f"https://www.reddit.com{submission.permalink}",
            "score": submission.score,
            "comments": []
        }

        # Get all comments including replies
        submission.comments.replace_more(limit=None)
        reddit_post["comments"] = [process_comment(comment) for comment in submission.comments if isinstance(comment, praw.models.Comment)]

        # Add new post to existing posts
        existing_posts.append(reddit_post)
        
        # Save all posts to JSON file
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(existing_posts, f, ensure_ascii=False, indent=2)
        print(f"Successfully stored Reddit post with ID: {submission.id}")

if __name__ == "__main__":
    get_thelastofus_posts()
