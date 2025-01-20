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

def analyze_post_sentiment(post_title):
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

def analyze_keywords(sentiment, sentence):
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

def retrieve_post_title():
    with open('../../data/processed/processed_reddit_data.json', 'r') as file:
        json_data = json.load(file)
        post_titles = json_data['post_titles']
        return post_titles

def retrieve_comment_body():
    with open('../../data/processed/processed_reddit_data.json', 'r') as file:
        json_data = json.load(file)
        comment_bodies = json_data['comment_bodies']
        return comment_bodies

def analyze_comment_sentiment(comment_body, parent_body):
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
    return sentiment_data['sentiment']

if __name__ == "__main__":    
    enhanced_data = []

    # handle posts
    post_titles = retrieve_post_title()
    for post_title in post_titles:
        sentiment = analyze_post_sentiment(post_title['title'])
        keywords = analyze_keywords(sentiment, post_title['title'])

        post_title['sentiment'] = sentiment
        post_title['keywords'] = keywords['keywords']
    
        enhanced_data.append(post_title)

    # handle comments
    comment_bodies = retrieve_comment_body()
    for comment_body in comment_bodies:
        sentiment = analyze_comment_sentiment(comment_body['body'], comment_body['parent_body'])

        keywords = analyze_keywords(sentiment, comment_body['body'])

        comment_body['sentiment'] = sentiment
        comment_body['keywords'] = keywords['keywords']

        enhanced_data.append(comment_body)
    
    output_path = '../../data/analyzed/analyzed_reddit_data.json'
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(enhanced_data, f, indent=4, ensure_ascii=False)
    
    print(f"\nEnhanced data saved to: {output_path}")