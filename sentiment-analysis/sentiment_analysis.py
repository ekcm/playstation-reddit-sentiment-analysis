import json

def conduct_sentiment_analysis(json_file_path):
    # Perform sentiment analysis on the processed data
    
    with open(json_file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        # Debug print to see the structure

        post_titles = json_data['post_titles']
        comment_bodies = json_data['comment_bodies']

        print("Post Titles:", post_titles)


if __name__ == "__main__":
    json_file_path = "../data/processed_reddit_data.json"
    conduct_sentiment_analysis(json_file_path)