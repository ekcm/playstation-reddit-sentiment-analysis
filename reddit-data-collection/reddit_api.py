import praw
import os
from dotenv import load_dotenv
from mongodb_handler import insert_reddit_post, check_post_exists

load_dotenv("../.env")

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
    }

def get_thelastofus_posts():
    subreddit = reddit.subreddit("thelastofus")
    query = 'review' # Look for posts that include the word 'review'

    for submission in subreddit.search(query, sort='relevance', time_filter='all', limit=1):
        reddit_post = {
            "id": submission.id,
            "title": submission.title,
            "created_UTC": submission.created_utc,
            "url": f"https://www.reddit.com{submission.permalink}",
            "score": submission.score,
            "comments": []
        }

        # check if id already exists in database
        if check_post_exists(submission.id):
            print(f"Post with ID {submission.id} already exists in database. Skipping...")
            continue

        # Get all comments including replies
        submission.comments.replace_more(limit=None)
        reddit_post["comments"] = [process_comment(comment) for comment in submission.comments if isinstance(comment, praw.models.Comment)]

        # Insert into MongoDB
        inserted_id = insert_reddit_post(reddit_post)
        if inserted_id:
            print(f"Successfully stored Reddit post in MongoDB with _id: {inserted_id}")

get_thelastofus_posts()
