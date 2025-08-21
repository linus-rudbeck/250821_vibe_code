import requests
from openai import OpenAI

PROMPT = """
Write me a poem about birds and bees
"""

LLM_BASE_URL="http://localhost:12434/engines/v1/chat/completions"

MODEL = "ai/smollm2"

def fetch_response(user_message):
    """Calls the LLM API and returns the response"""
    
    chat_request = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant. Please provide structured responses using markdown formatting. Use headers (# for main points), bullet points (- for lists), bold (**text**) for emphasis, and code blocks (```code```) for code examples. Organize your responses with clear sections and concise explanations.",
            },
            {"role": "user", "content": user_message},
        ],
        "temperature": 0,
    }

    headers = {"Content-Type": "application/json"}

    # Send request to LLM API
    response = requests.post(LLM_BASE_URL, headers=headers, json=chat_request)

    # Check if the status code is not 200 OK
    if response.status_code != 200:
        raise Exception(f"API returned {response.status_code}: {response.text}")

    # Parse the response
    chat_response = response.json()

    # Extract the assistant's message
    if chat_response.get("choices") and len(chat_response["choices"]) > 0:
        return chat_response["choices"][0]["message"]["content"].strip()

    raise Exception("No response choices returned from API")


def main():
    response = fetch_response(PROMPT)
    print("Response:")
    print(response)

if __name__ == "__main__":
    main()