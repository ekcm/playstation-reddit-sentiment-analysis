from fastapi import FastAPI, HTTPException
import json
from datetime import datetime
from typing import Optional, Dict
from enum import Enum
from collections import Counter
from pathlib import Path
from functools import lru_cache

app = FastAPI(
    docs="/",
)

class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

# Constants
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATA_FILE = Path("../../data/analyzed/analyzed_reddit_data.json")

@lru_cache()
def load_sentiment_data() -> list:
    """Load and cache the sentiment data."""
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, message="Sentiment data file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, message="Error parsing sentiment data")

def parse_date(date_str: Optional[str], is_end_date: bool = False) -> Optional[float]:
    """Parse date string to timestamp with validation."""
    if not date_str:
        return None
    
    try:
        if is_end_date:
            dt = datetime.strptime(f"{date_str} 23:59:59", DATETIME_FORMAT)
        else:
            dt = datetime.strptime(date_str, DATE_FORMAT)
        return dt.timestamp()
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid date format. Please use {DATE_FORMAT}"
        )


@app.get("/sentiment-analysis")
async def get_sentiment_analysis(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> Dict:
    """
    Get sentiment analysis with optional date range filtering.
    
    Args:
        start_date: Optional start date in YYYY-MM-DD format
        end_date: Optional end date in YYYY-MM-DD format
    
    Returns:
        Dict containing sentiment counts and date range info
    """
    # Parse dates
    start_timestamp = parse_date(start_date)
    end_timestamp = parse_date(end_date, is_end_date=True)
    
    # Load data
    data = load_sentiment_data()
    
    # Count sentiments within date range
    sentiment_counter = Counter()
    
    for item in data:
        created_time = item['created_UTC']
        
        # Skip if outside date range
        if (start_timestamp and created_time < start_timestamp) or \
           (end_timestamp and created_time > end_timestamp):
            continue
            
        sentiment_counter[item['sentiment']] += 1
    
    return {
        "date_range": {
            "start_date": start_date,
            "end_date": end_date
        },
        "sentiment_counts": {
            Sentiment.POSITIVE: sentiment_counter[Sentiment.POSITIVE],
            Sentiment.NEGATIVE: sentiment_counter[Sentiment.NEGATIVE],
            Sentiment.NEUTRAL: sentiment_counter[Sentiment.NEUTRAL]
        },
        "total": sum(sentiment_counter.values())
    }

@app.get("/keywords")
async def get_top_keywords_frequencies(sentiment: str) -> Dict:
    """
    Get keywords for a specific sentiment, sorted by frequency.
    
    Args:
        sentiment: Sentiment to filter by (positive/negative/neutral)
    
    Returns:
        Dict containing sorted keywords and their frequencies
    """
    
    # Load data
    data = load_sentiment_data()
    
    # Count keyword frequencies
    keyword_counter = Counter()
    
    for item in data:
        if item['sentiment'] == sentiment:
            keyword_counter.update(item['keywords'])
    
    # Sort keywords by frequency in descending order
    sorted_keywords = [
        {"keyword": kw, "frequency": freq}
        for kw, freq in keyword_counter.most_common()
    ]
    
    return {
        "sentiment": sentiment,
        "keywords": sorted_keywords,
        "total_keywords": len(sorted_keywords)
    }

@app.get("/top-posts")
async def get_top_posts() -> Dict:
    """
    Get all posts sorted by score in descending order.
    
    Returns:
        Dict containing sorted posts and total count
    """
    # Load data
    data = load_sentiment_data()
    
    # Filter for posts (items with 'title' field)
    posts = [item for item in data if 'title' in item]
    
    # Sort posts by score in descending order
    sorted_posts = sorted(
        posts,
        key=lambda x: x['score'],
        reverse=True
    )
    
    return {
        "posts": sorted_posts,
        "total_posts": len(sorted_posts)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)