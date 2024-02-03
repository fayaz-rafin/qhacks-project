import requests
import os
import dotenv

dotenv.load_dotenv()

headers = {"Authorization": f"Bearer {os.environ['CLOUDFLARE_API_KEY']}"}
CLOUDFLARE_BASE_URL = os.environ["CLOUDFLARE_BASE_URL"]
CLOUDFLARE_ACCOUNT_ID = os.environ["CLOUDFLARE_ACCOUNT_ID"]


def run(model: str, input: dict):
    response = requests.post(f"{CLOUDFLARE_BASE_URL}{model}", headers=headers, json=input)
    return response.json()


def generate_embeddings(text: str):
    model = "@cf/baai/bge-small-en-v1.5"
    input = {
        "text": text
    }
    output = run(model, input)
    return output


if __name__ == "__main__":
    input = "I am a test string"
    print(generate_embeddings(input))
