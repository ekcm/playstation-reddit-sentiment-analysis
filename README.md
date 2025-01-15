# playstation-reddit-sentiment-analysis

## Reddit Data Collection

This project was built for the purpose of learning how to scrape reddit data and analyze it using sentiment analysis.

### Setting up Python dependencies:
1. Initialize Python dependencies from Poetry with `poetry init`
2. Install dependencies with `poetry install`

### Setting up environment variables:
1. Create a .env file with the following variables:
```
CLIENT_ID=
CLIENT_SECRET=
USER_AGENT=<platform>:<app ID>:<version string> (by u/<Reddit username>)
MONGODB_URI=
MONGODB_DATABASE=
MONGODB_COLLECTION=
```
You can refer to Reddit API documentation on how to set up the Reddit variables

### Running the project:
1. Run `poetry shell` to enter into the virtual environment
2. Set up the MongoDB database by running `python mongodb_handler.py`. This will first verify if there is a connection to the MongoDB database and then create the database and collection if they don't already exist.
3. Run `python reddit_api.py`. This will scrape the reddit data and store it in the database. It will also check if the post already exists in the database and skip it if it does.
4. Run `python mongodb_handler.py`. This will export the data from the MongoDB database into a JSON file.

### Setting up Llama3.2:
1. Install Ollama

2. Once Ollama is installed, load llama3.2
```
ollama run llama3.2
```

3. Run the `test_ollama_request` function in `llm_handler.py`
``` 
python llm_handler.py
```
