import requests
import json

def test_ollama_request(url: str = 'http://localhost:11434/api/generate'):
    """
    Test if Ollama API can handle a simple generation request.
    """

    headers = {'Content-Type': 'application/json'}

    data = {
        "model": "llama3.2",
        "prompt": "Why is the sky blue?"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_text = response.text

    lines = response_text.strip().splitlines()
    responses = [json.loads(line)["response"] for line in lines]

    # Join the responses into a complete sentence
    result = ''.join(responses)

    return result

if __name__ == "__main__":
    print(test_ollama_request())