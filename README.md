# IAP - Sony Interactive Entertainment Comes to MIT

This is a small project for the IAP - Sony Interactive Entertainment Comes to MIT: The Nexus of Games and AI Course.
This project is a proof of concept to show how large language models can be used for sentiment analysis on social media.
Note: data is scraped from the [r/thelastofus](https://www.reddit.com/r/thelastofus/) subreddit

## Built With
* [Python](https://www.python.org/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [TypeScript](https://www.typescriptlang.org/)
* [Next.js](https://nextjs.org/)
* [Llama3.2](https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/) + [Ollama](https://github.com/ollama/ollama)
* [PRAW](https://praw.readthedocs.io/en/stable/)

## Setting up 

### Setting up environment variables:
1. Create a .env file in `/backend` with the following variables:
```
CLIENT_ID=
CLIENT_SECRET=
USER_AGENT=<platform>:<app ID>:<version string> (by u/<Reddit username>)
```
You can refer to Reddit API documentation on how to set up the Reddit variables for the application [here](https://old.reddit.com/prefs/apps/)

### Setting up Llama3.2:
1. Install Ollama
2. Once Ollama is installed, load llama3.2
```
ollama run llama3.2
```
3. Run ollama_config.py to check ollama is installed correctly
```
cd backend/src/sentiment_analysis
python ollama_config.py
```

### Run the shell script to scrape Reddit data, process the data, and analyze the sentiment of each post/comment/reply using llama3.2
```
chmod +x scripts/run_pipeline.sh
./scripts/run_pipeline.sh
```

### Start the application using Docker Compose
```
docker-compose up --build
```
You can access the frontend from `http://localhost:3000/`, which will visualize the insights generated from r/thelastofus subreddit.

## Screenshots
