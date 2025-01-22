from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
import json
from pathlib import Path
import time
import requests

# Get the backend directory path
backend_dir = Path(__file__).resolve().parents[2]

# Set up paths
data_dir = backend_dir / "data"
processed_dir = data_dir / "processed"
analyzed_dir = data_dir / "analyzed"

# Create directories if they don't exist
processed_dir.mkdir(parents=True, exist_ok=True)
analyzed_dir.mkdir(parents=True, exist_ok=True)

def wait_for_ollama(max_retries=5, retry_delay=2):
    """Wait for Ollama service to be ready"""
    for i in range(max_retries):
        try:
            response = requests.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                print("Successfully connected to Ollama")
                return True
        except requests.exceptions.ConnectionError:
            if i < max_retries - 1:
                print(f"Waiting for Ollama to be ready... (attempt {i + 1}/{max_retries})")
                time.sleep(retry_delay)
            continue
    raise Exception("Could not connect to Ollama service")

# Wait for Ollama to be ready
wait_for_ollama()

local_llm = "llama3.2"
llm = ChatOllama(
    model=local_llm,
    temperature=0,
    format="json"
)

def analyze_post_sentiment(post_title):
    max_retries = 3
    retry_delay = 2
    for i in range(max_retries):
        try:
            answer = llm.invoke(
                [SystemMessage(content='''
                You are a helpful assistant that analyzes the sentiment of a post title. 
                You understand that the title can be nuanced, and that it can only be positive, negative, or neutral.
                You will respond with the sentiment of the post title in the following format:
                {
                    "sentiment": "positive" | "negative" | "neutral",
                }
                ''')] +
                [HumanMessage(content=post_title)]
            )
            # Parse the JSON content and extract just the sentiment
            sentiment_data = json.loads(answer.content)
            return sentiment_data
        except Exception as e:
            if i < max_retries - 1:
                print(f"Error analyzing post sentiment, retrying... (attempt {i + 1}/{max_retries})")
                time.sleep(retry_delay)
            else:
                raise Exception(f"Failed to analyze post sentiment after {max_retries} retries: {str(e)}")

def analyze_keywords(sentiment, sentence):
    max_retries = 3
    retry_delay = 2
    for i in range(max_retries):
        try:
            answer = llm.invoke(
                [SystemMessage(content='''
                You are a helpful assistant that understands keywords in a sentence. 
                You are given a sentiment and a sentence.
                You are to respond with a list of keywords that must come from the sentence that explains the sentiment of the sentence.

                You will respond with the keywords in the following format:
                {
                    "keywords": ["keyword1", "keyword2", "keyword3"]
                }
                ''')] +
                [HumanMessage(content=f"Sentiment: {sentiment}, Sentence: {sentence}")]
            )
            keywords = json.loads(answer.content)
            return keywords
        except Exception as e:
            if i < max_retries - 1:
                print(f"Error analyzing keywords, retrying... (attempt {i + 1}/{max_retries})")
                time.sleep(retry_delay)
            else:
                raise Exception(f"Failed to analyze keywords after {max_retries} retries: {str(e)}")

def analyze_comment_sentiment(comment_body, parent_body):
    max_retries = 3
    retry_delay = 2
    for i in range(max_retries):
        try:
            answer = llm.invoke(
                [SystemMessage(content='''
                You are a helpful assistant that analyzes the sentiment of a comment body. 
                You understand that the body can be nuanced, and that it can only be positive, negative, or neutral.
                You will only use the parent body to help you understand the sentiment of the comment body.

                You will respond with the sentiment of the comment body in the following format:
                {
                    "sentiment": "positive" | "negative" | "neutral",
                }
                ''')] +
                [HumanMessage(content=f"Comment Body: {comment_body}, Parent Body: {parent_body}")]
            )
            # Parse the JSON content and extract just the sentiment
            sentiment_data = json.loads(answer.content)
            return sentiment_data
        except Exception as e:
            if i < max_retries - 1:
                print(f"Error analyzing comment sentiment, retrying... (attempt {i + 1}/{max_retries})")
                time.sleep(retry_delay)
            else:
                raise Exception(f"Failed to analyze comment sentiment after {max_retries} retries: {str(e)}")

if __name__ == "__main__":    
    enhanced_data = []
    
    try:
        # Read processed data
        input_file = processed_dir / "processed_reddit_data.json"
        with open(input_file, 'r') as f:
            data = json.load(f)
            
        total_posts = len(data['post_titles'])
        total_comments = len(data['comment_bodies'])
        total_items = total_posts + total_comments
        current_item = 0
            
        print(f"\nStarting sentiment analysis for {total_posts} posts and {total_comments} comments...")
            
        # Process post titles
        for idx, title in enumerate(data['post_titles'], 1):
            current_item += 1
            print(f"\rProcessing item {current_item}/{total_items} (Post {idx}/{total_posts})", end="", flush=True)
            sentiment = analyze_post_sentiment(title['title'])
            keywords = analyze_keywords(sentiment['sentiment'], title['title'])
            enhanced_data.append({
                'id': title['id'],
                'created_utc': title['created_UTC'],  
                'title': title['title'],
                'url': title['url'],
                'score': title['score'],
                'sentiment': sentiment['sentiment'],
                'keywords': keywords['keywords']
            })
            
        # Process comment bodies
        for idx, comment in enumerate(data['comment_bodies'], 1):
            current_item += 1
            print(f"\rProcessing item {current_item}/{total_items} (Comment {idx}/{total_comments})", end="", flush=True)
            sentiment = analyze_comment_sentiment(comment['body'], comment['parent_body'])
            keywords = analyze_keywords(sentiment['sentiment'], comment['body'])
            enhanced_data.append({
                'id': comment['id'],
                'created_utc': comment['created_UTC'],  
                'body': comment['body'],
                'parent_body': comment['parent_body'],
                'score': comment['score'],
                'sentiment': sentiment['sentiment'],
                'keywords': keywords['keywords']
            })
            
        print("\n")  # New line after progress counter
            
        # Save analyzed data
        output_file = analyzed_dir / "analyzed_reddit_data.json"
        with open(output_file, 'w') as f:
            json.dump(enhanced_data, f, indent=2)
            
        print(f"Successfully analyzed {len(enhanced_data)} items ({total_posts} posts and {total_comments} comments) and saved to {output_file}")
        
    except Exception as e:
        print(f"\nError during sentiment analysis: {str(e)}")