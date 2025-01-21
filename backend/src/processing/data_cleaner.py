import json

def retrieve_comments_body(json_data):
    """
    Retrieves both post titles and comment bodies from Reddit JSON data
    
    Args:
        json_data (dict): The Reddit JSON data containing posts and comments
        
    Returns:
        dict: A dictionary containing lists of post titles and comment bodies
    """
    retrieved_data = {
        'post_titles': [],
        'comment_bodies': []
    }
    
    # Create a mapping of comment IDs to their bodies
    comment_body_map = {}
    
    # Handle case where json_data might be a list of submissions
    submissions = json_data if isinstance(json_data, list) else [json_data]
    
    for submission in submissions:
        # Extract post title
        if isinstance(submission, dict) and 'title' in submission:
            post_dict = {
                'id': submission['id'],
                'title': submission['title'],
                'created_UTC': submission['created_UTC'],
                'url': submission['url'],
                'score': submission['score'],
            }
            retrieved_data['post_titles'].append(post_dict)
            comment_body_map[submission['id']] = submission['title']  # Store submission title for top-level comments
        
        # Extract comments
        comments = submission.get('comments', [])
        if isinstance(comments, list):
            for comment in comments:
                if isinstance(comment, dict) and 'body' in comment:
                    if comment['score'] > 10 and comment['body'] != '[deleted]':
                        # Store comment body in mapping
                        comment_body_map[comment['id']] = comment['body']
                        
                        # Process main comment
                        comment_dict = {
                            'id': comment['id'],
                            'body': comment['body'],
                            'created_UTC': comment['created_UTC'],
                            'score': comment['score'],
                            'parent_id': comment['parent_id'],
                            'parent_body': comment_body_map.get(comment['parent_id'], "Parent content not available")
                        }
                        retrieved_data['comment_bodies'].append(comment_dict)
                
                        # Process replies recursively
                        def process_replies(comment_data):
                            replies_list = comment_data.get('replies', [])
                            if isinstance(replies_list, list):
                                for reply in replies_list:
                                    if isinstance(reply, dict) and reply.get('score', 0) > 10 and reply.get('body') != '[deleted]':
                                        # Store reply body in mapping
                                        comment_body_map[reply['id']] = reply['body']
                                        
                                        reply_dict = {
                                            'id': reply['id'],
                                            'body': reply['body'],
                                            'created_UTC': reply['created_UTC'],
                                            'score': reply['score'],
                                            'parent_id': reply['parent_id'],
                                            'parent_body': comment_body_map.get(reply['parent_id'], "Parent content not available")
                                        }
                                        retrieved_data['comment_bodies'].append(reply_dict)
                                        # Recursively process nested replies
                                        process_replies(reply)
                        
                        process_replies(comment)
    
    return retrieved_data

def import_reddit_data(json_file_path):
    """
    Imports Reddit JSON data from a file and processes it to extract titles and comments
    
    Args:
        json_file_path (str): Path to the JSON file containing Reddit data
        
    Returns:
        dict: A dictionary containing lists of post titles and comment bodies
        
    Raises:
        FileNotFoundError: If the specified JSON file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            # Debug print to see the structure
            print("JSON Data Keys:", json_data.keys() if isinstance(json_data, dict) else "Data is a list")
            return retrieve_comments_body(json_data)
    except FileNotFoundError:
        print(f"Error: File not found at {json_file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_file_path}")
        return None

def save_to_json(data, output_path):
    """
    Save the retrieved data to a JSON file
    
    Args:
        data (dict): The data to save
        output_path (str): Path where to save the JSON file
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Data successfully saved to {output_path}")
    except Exception as e:
        print(f"Error saving data to {output_path}: {str(e)}")

if __name__ == "__main__":
    json_file_path = "../../data/raw/reddit_data.json"
    output_path = "../../data/processed/processed_reddit_data.json"
    
    retrieved_data = import_reddit_data(json_file_path)
    if retrieved_data:
        save_to_json(retrieved_data, output_path)
        print(f"Found {len(retrieved_data['post_titles'])} posts and {len(retrieved_data['comment_bodies'])} comments")