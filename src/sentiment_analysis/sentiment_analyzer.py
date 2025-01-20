from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
import json
import os

local_llm = "llama3.2"
llm = ChatOllama(
    model=local_llm,
    temperature=0,
    format="json"
)

system_message = SystemMessage(content='''
    You are a helpful assistant that analyzes the sentiment of a post title. 
    You understand that the title can be nuanced, and that it can only be positive, negative, or neutral.
    You will respond with the sentiment of the post title in the following format:
    {
        "sentiment": "positive" | "negative" | "neutral",
    }
''')

def analyze_sentiment(post_title):
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
    return sentiment_data['sentiment']

def analyze_keywords(sentiment, post_title):
    answer = llm.invoke(
        [SystemMessage(content='''
        You are a helpful assistant that understands keywords in a post title. 
        You are given a sentiment and a post title.
        You are to respond with a list of keywords that explains the sentiment of the post title.
        ''')] +
        [HumanMessage(content=f"Sentiment: {sentiment}, Post Title: {post_title}")]
    )

    keywords = json.loads(answer.content)
    return keywords

def retrieve_post_title():
    with open('../../data/processed/processed_reddit_data.json', 'r') as file:
        json_data = json.load(file)
        post_titles = json_data['post_titles']
        return post_titles

if __name__ == "__main__":
    post_titles = retrieve_post_title()
    
    for post_title in post_titles:
        sentiment = analyze_sentiment(post_title['title'])
        print(sentiment)
        keywords = analyze_keywords(sentiment, post_title['title'])
        print(keywords)

        post_title['sentiment'] = sentiment
        post_title['keywords'] = keywords
    
    enhanced_data = {
        'post_titles': post_titles
    }
    
    output_path = '../../data/analyzed/analyzed_reddit_data.json'
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(enhanced_data, f, indent=4, ensure_ascii=False)
    
    print(f"\nEnhanced data saved to: {output_path}")